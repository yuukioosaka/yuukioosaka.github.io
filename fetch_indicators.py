#!/usr/bin/env python3
"""
prompt.md で参照される主要6指標を yfinance から取得し、markdown に出力する。

表の行 = ベース指標(当日/前日/前日比率)、「年次ボラティリティ」列 = 各指標の専用VI(実測)。
専用VI:
    - 日経平均       → 日経VI (Yahoo無しのため ^N225 の1年HVで代用 ※推定)
    - S&P500          → VIX (^VIX)
    - ドル円          → ドル円1年HV (IV無しのため代用 ※推定)
    - 米10年債利回り  → MOVE指数 (^MOVE)
    - 日本国債10年債  → 日本国債VIX (^SPJGBV) ※利回りは FRED から直接取得
    - NY原油(WTI)     → OVX (^OVX)

日本国債10年債利回りは Yahoo に該当 ticker がないため、FRED の
IRLTLT01JPM156N (日本長期金利, OECD基準・月次) CSV を直接取得する。
"""
import sys
import io
from datetime import datetime

import yfinance as yf
import pandas as pd
from curl_cffi import requests as creq

# Windows コンソールでも UTF-8 で出力できるよう差し替え
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ベース指標: (表示名, カテゴリ, 価格ticker)
#   price_ticker が None なら、investing.com スクレイピングで日本国債10年債利回りを取得する。
BASES = [
    ("日経平均株価", "株式", "^N225"),
    ("S&P500", "株式", "^GSPC"),
    ("ドル円 (USD/JPY)", "為替", "USDJPY=X"),
    ("米10年債利回り", "金利・債券", "^TNX"),
    ("日本国債10年債利回り", "金利・債券", None),
    ("NY原油先物 (WTI)", "コモディティ", "CL=F"),
]

# 各指標の専用VI: (表示名 -> (VI ticker, VI表示名, VIの%表記フラグ))
#   ticker が None のVIは HV を計算する (price_ticker から直近1年HV)。
#   None(価格) の場合、その指標の年次ボラ列は HV 代用になる。
VI_MAP = {
    "日経平均株価": ("N225-HV", "日経VI (HV代用)", "^N225", True),
    "S&P500": ("^VIX", "VIX", "^VIX", True),
    "ドル円 (USD/JPY)": ("JPY-HV", "ドル円1年HV (IV代用)", "USDJPY=X", True),
    "米10年債利回り": ("^MOVE", "MOVE指数", "^MOVE", False),
    "日本国債10年債利回り": ("^SPJGBV", "日本国債VIX (S＆P/JPX)", "^SPJGBV", True),
    "NY原油先物 (WTI)": ("^OVX", "OVX", "^OVX", False),
}


def fetch_history(ticker: str) -> pd.Series:
    """最後の終値 Series を取得。失敗時は空 Series を返す。"""
    try:
        data = yf.Ticker(ticker)
        df = data.history(period="1y")
        if df.empty:
            return pd.Series(dtype=float)
        return df["Close"]
    except Exception:
        return pd.Series(dtype=float)


def fmt(value, *, percent: bool = False) -> str:
    """数値を整形。NaN や取得不可は空文字。"""
    if not isinstance(value, (int, float)) or pd.isna(value):
        return "-"
    if percent:
        return f"{value:.2f}%"
    return f"{value:,.2f}"


def compute_vol(series: pd.Series, window: int = 252) -> float:
    """直近 window 日間の日次リターンから年次(年率換算)ボラティリティを概算。"""
    if len(series) < 20:
        return float("nan")
    rets = series.pct_change().dropna()
    return rets[-window:].std() * (252 ** 0.5) * 100


def compute_annual_return(series: pd.Series) -> float:
    """直近1年の年次リターン(%)を算出。最初と最後の値から年率換算。"""
    if len(series) < 20:
        return float("nan")
    first = series.iloc[0]
    last = series.iloc[-1]
    if not first or pd.isna(first) or pd.isna(last):
        return float("nan")
    n = len(series)
    return ((last / first) ** (252 / n) - 1) * 100


def compute_sharpe(series: pd.Series, rfr: float = 0.0) -> float:
    """年次シャープレシオ。日次超過リターン標準偏差 × √252 。rfr は年率(%)。"""
    if len(series) < 20:
        return float("nan")
    rets = series.pct_change().dropna()
    daily_rfr = (rfr / 100.0) / 252.0
    excess = rets - daily_rfr
    std = excess.std()
    if not std or pd.isna(std):
        return float("nan")
    return (excess.mean() / std) * (252 ** 0.5)


def calc_jgb_price(yield_val, coupon: float = 0.8, years_to_maturity: int = 10):
    """利回り(%)から 100円額面あたりの固定利付債の参考価格を逆算する。

    (年1回利払いの簡易モデル。クーポン・残存期間は広く使われる近似値)
    戻り値: 価格(円)。入力が無効なら NaN。
    """
    if yield_val is None or pd.isna(yield_val):
        return float("nan")
    y = yield_val / 100.0   # % → 小数
    c = coupon / 100.0      # クーポン → 小数
    n = years_to_maturity
    price = (c * (1 - (1 + y) ** (-n))) / y + (100 / (1 + y) ** n)
    return round(price, 2)


def get_vi_value(vi_ticker, price_ticker) -> float:
    """専用VIの値を返す。ticker名が '-HV' 終わりなら価格系列から1年HVを計算。"""
    if vi_ticker.endswith("-HV"):
        series = fetch_history(price_ticker)
        return compute_vol(series, window=252)
    series = fetch_history(vi_ticker)
    if series.empty:
        return float("nan")
    return series.iloc[-1]


def fetch_japan_10y():
    """FRED から日本国債(10年)長期金利を直接取得する。

    FREDシンボル: IRLTLT01JPM156N (Japan Long-Term Government Bond Yield, OECD)。
    FREDは月次系列のため、最新月・前月の利回りと前月比を返す。
    戻り値: (最新利回り%, 前月利回り%, 前月比%). 取得失敗時は (NaN, NaN, None)。
    """
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=IRLTLT01JPM156N"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    }
    try:
        res = creq.get(url, headers=headers, timeout=20, impersonate="chrome")
        if res.status_code != 200:
            return float("nan"), float("nan"), None
        rows = [r for r in res.text.strip().splitlines() if r and "," in r]
        if len(rows) < 2:
            return float("nan"), float("nan"), None
        header = rows[0]
        if "IRLTLT01JPM156N" not in header:
            return float("nan"), float("nan"), None
        try:
            last = float(rows[-1].split(",")[1])
            prev = float(rows[-2].split(",")[1])
        except (IndexError, ValueError):
            return float("nan"), float("nan"), None
        pct = ((last / prev) - 1) * 100 if prev else None
        return last, prev, pct
    except Exception:
        return float("nan"), float("nan"), None


def main():
    print("🔄 主要6指標と専用VIを yfinance から取得中...\n")
    rows = []
    jgb_price_str = "-"   # 日本国債10年の100円額面あたり参考価格

    for name, category, price_ticker in BASES:
        vi_ticker, vi_label, vi_price_tc, vi_percent = VI_MAP[name]
        vi_value = get_vi_value(vi_ticker, vi_price_tc)

        # ベース指標の当日/前日値
        scraped_pct = None
        if price_ticker:
            series = fetch_history(price_ticker)
            if series.empty:
                today = prev = float("nan")
            else:
                today = series.iloc[-1]
                prev = series.iloc[-2] if len(series) >= 2 else float("nan")
        else:
            # 日本国債10年債利回りは investing.com からスクレイピング
            today, prev, scraped_pct = fetch_japan_10y()

        # 年次リターン / シャープレシオ (価格系列がある指数系のみ算出、利回り系は除外)
        annual_ret = float("nan")
        sharpe = float("nan")
        if price_ticker and name not in ("米10年債利回り", "日本国債10年債利回り"):
            annual_ret = compute_annual_return(series)
            sharpe = compute_sharpe(series)

        # 利回り系(^TNX, 日本10年債)は % 表記
        percent_base = (price_ticker == "^TNX") or (price_ticker is None)
        pct = scraped_pct
        if pct is None and isinstance(today, (int, float)) and isinstance(prev, (int, float)) \
                and prev and not pd.isna(today) and not pd.isna(prev):
            pct = ((today / prev) - 1) * 100

        # 年次レンジ (σ1.0): 当日値(以上)を基準に ±VI%   ※VI が % 表示前提
        if isinstance(today, (int, float)) and not pd.isna(today) \
                and not (isinstance(prev, (int, float)) and pd.isna(prev)) \
                and isinstance(vi_value, (int, float)) and not pd.isna(vi_value) and vi_value > 0:
            lo = today * (1 - vi_value / 100.0)
            hi = today * (1 + vi_value / 100.0)
            rng = f"{fmt(lo, percent=percent_base)} 〜 {fmt(hi, percent=percent_base)}"
        else:
            rng = "-"

        # 日本国債10年債は 100円額面あたりの参考価格も算出 (クーポン0.8%・残存10年想定)
        if name == "日本国債10年債利回り":
            p = calc_jgb_price(today) if isinstance(today, (int, float)) and not pd.isna(today) else float("nan")
            if not pd.isna(p):
                jgb_price_str = f"{p:,.1f}円"  # 100円額面あたり参考価格
                print(f"       → 100円額面あたり参考価格: {jgb_price_str}")

        rows.append({
            "カテゴリ": category, "指標": name,
            "当日": fmt(today, percent=percent_base),
            "前日": fmt(prev, percent=percent_base),
            "前日比率": f"{pct:.2f}%" if pct is not None else "-",
            "年次リターン": f"{annual_ret:.2f}%" if not pd.isna(annual_ret) else "-",
            "年次ボラティリティ": f"{vi_value:.1f}%" if not pd.isna(vi_value) else "-",
            "シャープレシオ": f"{sharpe:.2f}" if not pd.isna(sharpe) else "-",
            "年次レンジ": rng,
        })
        print(f"  ✅ {name:<24} 当日={fmt(today, percent=percent_base):>12} VI({vi_label})={fmt(vi_value, percent=True)}")

    df = pd.DataFrame(rows)

    # ---- markdown 出力 ----
    today_str = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append("## 📊 市場指標サマリー")
    lines.append(f"\n_取得日時: {today_str} ・ データソース: Yahoo Finance (yfinance)_")
    lines.append("※ 年次ボラティリティ = 各指標の専用VI実測値\n")
    lines.append("| カテゴリ | 指標 | 当日 | 前日 | 前日比率 | 年次リターン | 年次ボラティリティ | シャープレシオ | 年次レンジ(σ1.0) |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for _, r in df.iterrows():
        lines.append(
            f"| {r['カテゴリ']} | {r['指標']} | {r['当日']} | {r['前日']} | "
            f"{r['前日比率']} | {r['年次リターン']} | {r['年次ボラティリティ']} | "
            f"{r['シャープレシオ']} | {r['年次レンジ']} |"
        )

    # 注記 (各指標のVI対応)
    lines.append("\n### 専用VIの対応と注記")
    vi_note = {
        "日経平均株価": "年次ボラ= 日経VI (Yahooに日経VI無しのため ^N225 の直近1年HV=28.6%で代用 ※推定)。\n  - 正確値は https://www.nikkei.com/marketdata/quote/NK225VI/ を参照",
        "S&P500": "年次ボラ= VIX (^VIX)",
        "ドル円 (USD/JPY)": "年次ボラ= ドル円1年HV (通貨IV無しのため代用 ※推定)。正確なIVはCboe/FXブローカー参照",
        "米10年債利回り": "年次ボラ= MOVE指数 (^MOVE)",
        "日本国債10年債利回り": ("年次ボラ= 日本国債VIX (^SPJGBV)。\n"
            "  - 利回り値は FRED (IRLTLT01JPM156N) から直接取得。FREDは月次系列のため、\n"
            "    表の『当日/前日/前日比率』はそれぞれ『最新月/前月/前月比』となる。\n"
            f"  - 100円額面あたり参考価格(クーポン0.8%・残存10年想定) = 約{jgb_price_str}"),
        "NY原油先物 (WTI)": "年次ボラ= OVX (^OVX)",
    }
    for k, v in vi_note.items():
        lines.append(f"- **{k}**: {v}")
    lines.append("\n※ HV は専用VI/IVがYahooに存在しない指標の代用値 (実測ボラティリティ)。")
    lines.append("※ HV代用 = 直近1年(約252営業日)の日次リターン標準偏差 × √252 で年率換算。")
    lines.append("※ 年次レンジ = 当日値 ± 年次ボラティリティ(VI%) の1σレンジ (※推定/概算)。")
    lines.append("※ 年次リターン = 直近1年の初値→終値から年率換算。シャープレシオ = 日次超過リターンの年次化(リスクフリーレート0%想定)。")
    lines.append("※ 年次リターン/シャープレシオは株式・為替・コモディティの価格系指標のみ算出(利回り系は除外)。")

    md = "\n".join(lines) + "\n"

    # ファイル保存
    out_path = "market_summary.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"\n✅ 出力完了: {out_path}")
    print("-----------------------------------------")
    print(md)


if __name__ == "__main__":
    main()
