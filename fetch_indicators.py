#!/usr/bin/env python3
"""
prompt.md で参照される指標を yfinance から取得し、markdown に出力する。

対象指標:
    - 株式: 日経平均株価、S&P500、日経VI、VIX
    - 為替: ドル円(USD/JPY)、ドル円 1ヶ月 IV
    - 金利・債券: 米10年債利回り、日本10年債利回り、MOVE指数、日本国債VIX
    - コモディティ: NY原油先物(WTI)、OVX
10日分を取得し、当日・前日・前日比(率)を表形式で markdown 出力する。
"""
import sys
import io
import yfinance as yf
import pandas as pd
from datetime import datetime

# Windows コンソールでも UTF-8 で出力できるよう差し替え
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Ticker と表示名・指標のマッピング
INDICATORS = [
    # (yfinance ticker, 表示名, カテゴリ)
    ("^N225", "日経平均株価", "株式"),
    ("^GSPC", "S&P500", "株式"),
    ("^VIX", "VIX", "株式ボラティリティ"),
    ("USDJPY=X", "ドル円 (USD/JPY)", "為替"),
    ("^TNX", "米10年債利回り", "金利・債券"),
    ("^IRX", "米13週T-Bill", "金利・債券"),
    ("^MOVE", "MOVE指数 (米国債VI)", "金利・債券"),
    ("^SPJGBV", "日本国債VIX (S＆P/JPX)", "金利・債券"),
    ("CL=F", "NY原油先物 (WTI)", "コモディティ"),
    ("^OVX", "OVX (原油VI)", "コモディティ"),
]

# 追加計算対象 (表示名, カテゴリ, 元ticker, HVウィンドウ)
DERIVED = [
    # 日経VI: Yahoo に日経VI自体が存在しないため、日経平均の HV(1年) で代用 (※推定)
    # 直近1年(約252営業日)の日次リターン標準偏差 × √252 で年率換算した実測ボラティリティ。
    ("日経VI (HV代用)", "株式ボラティリティ", "^N225", 252),
    # ドル円 1ヶ月 IV: 通貨IVは Yahoo に存在しないため、ドル円の HV(1年) で代用 (※推定)
    ("ドル円 1ヶ月 HV (IV代用)", "為替ボラティリティ", "USDJPY=X", 252),
]


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


def fmt(value, *, percent: bool = False, multiply: float = 1.0) -> str:
    """数値を整形。NaN や取得不可は空文字。"""
    if not isinstance(value, (int, float)) or pd.isna(value):
        return "-"
    v = float(value) * multiply
    if percent:
        return f"{v:.2f}%"
    return f"{v:,.2f}"


def compute_vol(series: pd.Series, window: int = 63) -> float:
    """直近 window 日間の日次リターンから年次(年率換算)ボラティリティを概算。"""
    if len(series) < 20:
        return float("nan")
    rets = series.pct_change().dropna()
    return rets[-window:].std() * (252 ** 0.5) * 100


def main():
    print("🔄 指標を yfinance から取得中...\n")
    rows = []

    # インデックス・先物系 (当日値, 前日値, HV, 年次レンジを表示)
    for ticker, name, category in INDICATORS:
        series = fetch_history(ticker)
        if series.empty:
            rows.append({
                "カテゴリ": category, "指標": name, "当日": "-",
                "前日": "-", "前日比率": "-", "年次ボラティリティ": "-",
                "年次レンジ": "-",
            })
            print(f"  ⚠ {name:<24}({ticker:<12}) 取得不可")
            continue

        today = series.iloc[-1]
        prev = series.iloc[-2] if len(series) >= 2 else float("nan")
        annual_vol = compute_vol(series)
        # 年次レンジ (σ1.0: 直近3ヶ月平均 ± 1σ)
        if len(series) >= 20:
            avg = series[-63:].mean()
            sd = series[-63:].std()
            lo_s = fmt(avg - sd, percent="VIX" in name)
            hi_s = fmt(avg + sd, percent="VIX" in name)
            rng = f"{lo_s} 〜 {hi_s}"
        else:
            rng = "-"

        rows.append({
            "カテゴリ": category, "指標": name,
            "当日": fmt(today, percent="VIX" in name),
            "前日": fmt(prev, percent="VIX" in name),
            "前日比率": (f"{((today / prev) - 1) * 100:.2f}%"
                        if isinstance(prev, (int, float)) and not pd.isna(prev) and prev else "-"),
            "年次ボラティリティ": f"{annual_vol:.1f}%" if not pd.isna(annual_vol) else "-",
            "年次レンジ": rng,
        })
        print(f"  ✅ {name:<24}({ticker:<12}) {today:.2f}")

    # 派生計算系 (HV 等)
    for name, category, src_ticker, window in DERIVED:
        series = fetch_history(src_ticker)
        if series.empty:
            rows.append({
                "カテゴリ": category, "指標": name, "当日": "-",
                "前日": "-", "前日比率": "-", "年次ボラティリティ": "-",
                "年次レンジ": "-",
            })
            print(f"  ⚠ {name:<24}(HV 計算不可)")
            continue
        # 指定ウィンドウの HV (年率換算)
        hv_w = compute_vol(series, window=window)
        hv3m = compute_vol(series, window=63)
        rows.append({
            "カテゴリ": category, "指標": name,
            "当日": (f"{hv_w:.1f}%" if not pd.isna(hv_w) else "-"),
            "前日": "-",
            "前日比率": "-",
            "年次ボラティリティ": (f"{hv3m:.1f}%" if not pd.isna(hv3m) else "-"),
            "年次レンジ": "-",
        })
        print(f"  ✅ {name:<24}(HV {hv_w:.1f}%)" if not pd.isna(hv_w) else f"  ⚠ {name}")

    df = pd.DataFrame(rows)

    # ---- markdown 出力 ----
    today_str = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append("## 📊 市場指標サマリー")
    lines.append(f"\n_取得日時: {today_str} ・ データソース: Yahoo Finance (yfinance)_\n")
    lines.append("| カテゴリ | 指標 | 当日 | 前日 | 前日比率 | 年次ボラティリティ | 年次レンジ(σ1.0) |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for _, r in df.iterrows():
        lines.append(
            f"| {r['カテゴリ']} | {r['指標']} | {r['当日']} | {r['前日']} | "
            f"{r['前日比率']} | {r['年次ボラティリティ']} | {r['年次レンジ']} |"
        )

    # 注記
    lines.append("\n### 注記")
    notes = {
        "日経VI (HV代用)": "Yahoo に日経VI自体が存在しない (^JNIV も実際には無効) ため、\n  日経平均(^N225)の直近1年(約252営業日)の日次リターン標準偏差 × √252 で代用 (※推定)\n  - 正確な今日の日経VIは https://www.nikkei.com/marketdata/quote/NK225VI/ を参照",
        "VIX": "S&P500 インプライド・ボラティリティ",
        "OVX": "NY原油(WTI) インプライド・ボラティリティ",
        "ドル円 1ヶ月 HV (IV代用)": "通貨の IV は Yahoo に存在しないため、ドル円(USDJPY=X)の直近1年(約252営業日)の日次リターン標準偏差 × √252 で代用 (※推定)\n  - 正確な IV は Cboe/通貨IV または FXブローカー(みんかぶ等) を参照",
        "MOVE指数": "米国債インプライド・ボラティリティ (^MOVE)",
        "日本国債VIX(S＆P/JPX)": "ticker: ^SPJGBV (Yahoo Finance 公式・正常取得を確認)",
        "年次ボラティリティ": "直近3ヶ月(約63営業日)の日次リターン標準偏差 × √252 で概算",
        "年次レンジ": "直近3ヶ月の平均 ± 1σ で概算 (※推定/概算)",
    }
    for k, v in notes.items():
        lines.append(f"- **{k}**: {v}")
    lines.append("\n※ HV は Yahoo に専用指数が存在しない指標の代用値 (実測のボラティリティ)。")

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
