---
layout: post
title: PMBOK 7→8 変更内容まとめ
date: 2026-08-08 00:00:00 +0900
excerpt: PMBOK第8版(2025年リリース)への変更点の整理。第7版の12の原則・8つのパフォーマンス領域をベースに、AIや新規領域への拡張が行われた。
---

- 2025年11月にPMIが発表したPMBOK第8版は、第7版(2021年)の原則ベースアプローチを踏襲しつつ、実務家からの「抽象的すぎる」という批判を受けてプロセスの具体性を復活させた、いわば第6版と第7版のハイブリッド型改訂である。

- 構造面での最大の変化は3点。第一に、12あった原則が6原則(Holistic View、Focus on Value、Embed Quality、Accountable Leader、Integrate Sustainability、Empowered Culture)に統合され、AI時代を見据えサステナビリティが新規原則として加わった一方、TailoringとRiskは独立原則から姿を消し、それぞれ独立章とパフォーマンスドメインへ格下げされた。第二に、8つあったパフォーマンスドメイン(Stakeholders、Team、Development Approach and Life Cycle等)が7つ(Governance、Scope、Schedule、Finance、Stakeholders、Resources、Risk)に再編され、旧来のナレッジエリアに近い機能軸に回帰した。第三に、第7版で本体から完全排除され別冊「Process Groups: A Practice Guide」に追いやられていた49プロセスが、40の非規範的プロセスとして本体に復活し、7ドメイン×5フォーカスエリア(旧プロセスグループの改称)の格子構造に組み込まれた。

- 内容面では、AI活用・サステナビリティ・ガバナンスの記述が大幅拡充され、付録にはAI(X3)と調達(X4)が新設された。品質・コミュニケーション・調達は独立ドメインでなくなり、それぞれGovernance・Stakeholders・付録に統合された。プロジェクトの定義自体にも「価値創出」という文言が明示的に追加され、単なる成果物完成から価値提供へと焦点が移行している。

- PMP試験は2026年7月9日に第8版準拠へ移行予定で、Business Environmentドメインの比重が大幅増加する見込み。

```tsv
カテゴリー	第7版(12原則)	第8版(6原則)	状態
価値提供システム	価値創出	価値創出	同じ
価値提供システム	プロジェクト環境	プロジェクト環境	同じ
原理原則	Stewardship	Be an Accountable Leader 	統合。誠実性・信頼性・コンプライアンスという「委任された責任」の概念がリーダーシップの説明責任に吸収
原理原則	Leadership	Be an Accountable Leader	統合。リーダーシップ行動の実践がStewardshipと合流し1原則化
原理原則	Team	Build an Empowered Culture	統合。協働的チーム環境の構築が「権限を与えられた文化」というより広い概念に拡張 
原理原則	Adaptability & Resilience	Build an Empowered Culture	統合。変化への適応力が文化醸成の一要素として再配置
原理原則	Stakeholders	Adopt a Holistic View	統合。ステークホルダーとの積極的関与が全体視点の一部に
原理原則	Systems Thinking	Adopt a Holistic View	統合。システム間相互作用の認識がそのままHolistic Viewの中核概念に 
原理原則	Complexity	Adopt a Holistic View	統合。複雑性への対応がHolistic Viewの実践的側面として吸収
原理原則	Change	Adopt a Holistic View	統合。変化を可能にする働きかけがHolistic Viewの一要素に
原理原則	Value	Focus on Value	継続。原則ラベル・趣旨ともほぼ同一で存続
原理原則	Quality 	Embed Quality	継続。「プロセスと成果物に品質を組み込む」という原文の趣旨を維持し名称のみ微調整
原理原則	Tailoring	✗ 消滅	原則層から除外。第8版Part2第3章「Tailoring」として独立章に格上げされ、単一原則としては扱われなくなった(格下げというより「独立章への昇格」が実態)
原理原則	Risk	✗ 消滅	原則層から除外。第8版Part2「Project Management Performance Domains」の1つ「Risk Performance Domain」として存続。原則からドメインへ移動
原理原則	(なし)	Integrate Sustainability 	新設。第7版に対応する原則・概念なし。サステナビリティを全プロジェクト領域に統合する原則として新規追加
ライフサイクル	Part2内「Development Approach and Life Cycle」ドメイン(8ドメインの1つ)	Part1「4. Project Life Cycles」独立章	位置移動+格上げ。Part2(Guide)のドメインから、Part1(Standard)の独立章に昇格。予測/適応/ハイブリッドの開発アプローチの記述内容はほぼ継続
ライフサイクル	Process Groups(本体に不在、別冊「Process Groups: A Practice Guide」のみに存在)	4.5 Project Management Focus Areas(Initiating/Planning/Executing/M&C/Closing)	復活・統合。別冊で温存されていたプロセスグループが、名称を変え本体に正式統合
ライフサイクル	Part2第4章「Models, Methods, and Artifacts」	Part2第4章「Inputs and Outputs」+第5章「Tools and Techniques」	分離・具体化。1つの参照章がITTO復活に伴い2つの専門参照章に分割
パフォーマンスドメイン	Stakeholders	Stakeholders	継続。名称・趣旨ともほぼ同一。第8版ではコミュニケーション機能も統合され範囲がやや拡大
パフォーマンスドメイン	Team	Resources	統合・改称。Resourcesドメインの構成プロセスはPlan Resource Management、Acquire Resources、Develop Team、Manage Team、Control Resourcesなど、人material・設備を含む管理機能に拡張 Hksmnow
パフォーマンスドメイン	Planning	(単一ドメインへ非対応、複数ドメインに分散)	⚠️要修正:単純な「Schedule」への改称ではなく、Plan Quality ManagementはGovernance(QA)とScopeプロセスに吸収、Define/Sequence Activities、Estimate DurationsはDevelop Scheduleに吸収など、Governance・Scope・Schedule・Financeに機能分散 BrainBOK
パフォーマンスドメイン	Project Work	Governance	統合・改称(推定)。Project Work domainは実行プロセスの組織化、環境への適合、コミュニケーションの明確化に焦点を当てており、これが「ルールの設定と監督」を担うGovernanceドメインに再編されたと推測される。ただし公式な1対1対応の明記は未確認 Substack
パフォーマンスドメイン	Delivery	Scope	統合・改称。Delivery domainは要件・スコープ・品質期待を実際の成果に変換し、戦略目標への貢献とステークホルダー要件充足を確保する役割を担っており、この「何を届けるか」の概念がScopeドメインへ再編 Substack
パフォーマンスドメイン	Measurement	Finance	改称(推定)。Measurement domainはプロジェクト進捗の評価、パフォーマンス指標の評価、データドリブンな意思決定を扱う領域だが、第8版ではFinance TrustEd Institute domainはPlan Financial Resources、Estimate Costs、Determine Budget、Control Costs、Perform Financial Closureといったプロセスで構成されており、コスト測定面はFinanceに集約。ただしKPIやパフォーマンス測定全般は複数ドメイン(特にGovernance)に分散した可能性が高く、Finance単独への統合は簡略化された対応関係 Hksmnow
パフォーマンスドメイン	Uncertainty	Risk	改称。Risk domainはPlan Risk Management、Identify Risks、Analyse Risks、Plan Risk Responses、Implement Risk Responses、Monitor Risksで構成され、不確実性対応という趣旨は継続しつつ名称をより直接的な「
テーラリング	テーラリング	テーラリング	同じ
```
