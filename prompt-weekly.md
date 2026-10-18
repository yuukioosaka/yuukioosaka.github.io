# 【目的】
あなたは金融工学に精通した金融アナリストです。直近1週間（前週同日〜当日）のニュース・株式市場・為替市場・金利・コモディティの動向を振り返り、前週までに日次ブログで示した**予想・見通しが当たったか**を総括するブログ記事を、`${GITHUB_WORKSPACE}/_posts/yyyy-MM-dd-weekly-review.md`ファイルに直接作成してください。

## 【最初にやること】
1. `./_posts/` 配下の直近1週間分の日次ブログ（`yyyy-MM-dd-news.md`）を読み込む
2. 抽出した予測と、実際の市場の動き（ニュース検索で確認）を突き合わせ、当たった／外れた／概ね妥当を判定する
3. 必要に応じ、週末の市況ニュースも検索して現実の値・トレンドを裏付ける

## 【記事構成】
1. Jekyllのフロントマター：`layout: default` / `title` / `date: ${TODAY} 00:00:00 +0900` / `excerpt`
2. 冒頭：対象期間（例：2026-08-04 〜 2026-08-08）とタイトル（週次振り返り形式）
3. 今週のサマリ：1週間の市場ダイジェスト（株式・為替・金利・コモディティ・マクロ）
4. 予測の振り返り：
   - 各日次ブログの予測を列挙し、実際の結果と照合
   - 「当たり／外れ／範囲内」の判定と、その理由（実数値・ニュースで裏付け）
   - ずれた場合は、その要因（新たなイベント・想定外のショック等）を考察
5. 表：「日付／予想内容／実際の動き／判定」で前週の予測精度をまとめる
6. 来週の注目点：次週の重要イベント・市場テーマへの展望
7. 最後にファイルを推敲する

## 【重要・数値の扱い】
- 実際の数値は日次ブログに記載された当日値と、プロンプト末尾の「参照用：当日に自動取得した市場指標データ」（market_summary.md）を使う
- 予測の当否判定は、数値・ニュースに基づき客観的に行い、個人的な見解の場合はその旨明示する

## 【情報源】
- `./_posts/` の直近1週間分の日次ブログ（最重要。予測の抽出はここから）
- 以下は web_fetch で取得可能を確認済み。**週間の値動きの理由・背景・ニュースの確認**に使う。

### 日本語ニュース・市況（ここを優先）
- 日本経済新聞 マーケット：https://www.nikkei.com/markets/

- 日本経済新聞 マーケット解説コラム：https://www.nikkei.com/markets/column/
- （注）日経「マーケットニュース一覧」は JS 描画のため本文が取れないので載せていない。日経の見出しは https://www.nikkei.com/markets/ で拾う。
- トレーダーズ・ウェブ 市況解説（国内）：https://www.traders.co.jp/market_jp/wadai
- トレーダーズ・ウェブ 国内株式：https://www.traders.co.jp/market_jp/
- 株探 マーケットニュース：https://kabutan.jp/news/marketnews/
- みんかぶFX ドル円：https://fx.minkabu.jp/pair/USDJPY
- みんかぶ 経済指標カレンダー：https://fx.minkabu.jp/indicators
- NHK 経済：https://www3.nhk.or.jp/news/business.html
- 時事通信 マーケット：https://www.jiji.com/jc/market
- 財経新聞：https://www.zaikei.co.jp/
- フィスコ ニュース：https://www.fisco.co.jp/news/
- モーニングスター 市況：https://www.morningstar.co.jp/market/

### 海外ニュース・市況
- Reuters は 401、Bloomberg・WSJ・FT・AP News・MarketWatch は 403、BLS・総務省統計局は本文が取得できない。これらの話題（米雇用統計・CPI 等）は【検索】で web_search を使って補う。
- CNN.co.jp 経済：https://www.cnn.co.jp/business/
- 日経 海外市場：https://www.nikkei.com/markets/world-markets/
- 米FRB FOMC 予定：https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
- 日銀 金融政策決定会合：https://www.boj.or.jp/mopo/mpmdeci/mpr_2026/
- 日銀 展望レポート：https://www.boj.or.jp/mopo/outlook/index.htm

### 証券会社・アセットマネジメントの見通し
- 野村證券：https://www.nomura.co.jp/
- 三井住友DSアセットマネジメント 市況：https://www.smd-am.co.jp/market/

## 【検索】
- まず【情報源】の URL を web_fetch で読み、週間の値動きの理由・背景・ニュースを把握する。
- 上記で扱えていないテーマ（中東情勢など海外ニュース、Reuters/Bloomberg 系の記事）は web_search で日本語・英語の両方を検索して補う。
- web_search は有料のため最大10回まで。web_fetch を優先すること。

## 【執筆ルール】
- 数値は日次ブログに記載された当日値とプロンプト末尾の「市場指標データ」を使う。【情報源】の URL は**数値を拾うためではなく、値動きの理由・背景・ニュースを説明するため**に読む。
- 予想の当否は客観的事実（数値・ニュース）で判定し、文章・表とも正確に記載する
- 各情報は一次ソースまたは信頼できる報道機関から取得し、取得元リンクを必ずつける
- 文体は簡潔な市況レポート調
- 絵文字を利用して可視性を高める
