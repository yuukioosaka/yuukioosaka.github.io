---
layout: default
title: AWSは高い！
date: 2022-09-23 00:00:00 +0900
excerpt: 円安によりAWSコストが上昇。サーバーレス化やAutoscaling、SPOTインスタンスなどによるコスト削減策をまとめる。
---

# AWS高すぎ問題

現在円安で1ドル142円前後となっている。1ドル110円台にAWSは安い！とか思ってコスト削減を狙って社内システムをコストをかけて移行した企業は、円安により30%以上値上がりした結果、AWSへの移行を後悔されていると思う。

とはいっても改めてサーバーを社内システムにも戻すわけにはいかない。どのような対策が考えられるだろうか。

## 想定するアーキテクチャー（こうした構成がたくさんある想定）：

![enyasu](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjI3fF3UiyJof0Ts44HwaaLlrWA9zSF3PWaMsVARTDMcbjbEOOwDpmmOyKpq-AymVJ0uZVr2Hjw1GgZQM3HqpDh6eR1Iy4B6jTDsA7o7gpYm31g9cCf_E4o2jwDt5NAIFBPgT8PeotJRe0ylmS6nBePFgJOmzx2nw1_a2ATM0hVtyN2hNREE2a06qBb/w454-h115/enyasu-%E3%83%9A%E3%83%BC%E3%82%B82.drawio.png)

## ①EC2を利用せずフルサーバーレス（SPA/S3/APIGateway/Lamda/Dynamodb）にアーキテクチャーを変更する

![enyasu](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhGIJ92oo-5mLWrZ4plHOmhvnBmrdqud1EUMfixtiRwWHEOCRuDd07UbDdnU8r7rF6ri6h1NZzCkPBJK5-pIpV9PAPLLRfjroyUruk4mxg1L_W7eOUFATpKPxPxx_-4SdDk_-KicKxRsxr2Bga-Rf-LQj1qBVYhL2LseeWlQEsIJDjl-csgqU1FXVib/w630-h228/enyasu-Page-1.drawio.png)

JavaやASP.NETなどのWebアプリケーションは高価なインスタンスを必要とするEC2やBeanstalk、RDSなどのインスタンスで動かさざるを得ない。
プログラムを根本的に書き換えることでインスタンスを利用しないフルサーバーレスアプリケーション（SPA/S3/APIGateway/Lamda/Dynamodb）を変更する。

- メリット：大幅なコスト削減、信頼性の向上が可能。サーバーレスでは利用量に応じた支払いになる。一般的な業務アプリケーションの利用時間（年の1/4程度でリソース利用率30%）からするとサーバーにかかわるコストは1/10程度のコストまで削減可能
- デメリット：アプリケーション再作成への初期投資がかかりすぎる。また、サーバーレスアーキテクチャーに通じたSEの調達も困難。
- 対象：更改タイミングなどが来ているアプリケーションの場合などにオススメ

## ②Autoscalingアーキテクチャーに変更して、サーバーをできる限り落とす。また、思い切ってSPOTインスタンスにしてしまう

![enyasu](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi8vpKAYcSoGLTbO61-ck9I4Rjw_AEdEvLjYEFnjPOOOdCu9VqSvymXGfbl2EtnTUuulFclBgYBYq2fxj7nedzWSyHWQaZijTF9hxYuf1aL0rVhOGiPB0jATRZD8IFO0reFU0fO9XsK2ViJklaEDodJldBoVKK3YSZ44EhRofHxmRpPTDs9seGOLRaF/w511-h351/enyasu-%E3%83%9A%E3%83%BC%E3%82%B83.drawio.png)

EC2の契約は通常の契約から大幅に割り引いた（90-80%値引き）SPOTインスタンスというものが存在する。SPOTインスタンスでサーバーを起動することでコストを大幅に削減することができる。ただし、SPOTインスタンスはAWSの要求によりサーバーが停止されるという大きなデメリットが存在する。これに対応するためサーバー停止時に再度起動するなどのAutoscalingアーキテクチャーの導入、停止をユーザーに検知させないためのALBを導入する。

- メリット：EC2インスタンス利用量のコスト削減が可能。
- デメリット：停止をユーザーに検知させないためALB利用のためのサーバー構成変更が必要。インスタンス停止イベントを受け取り、ALBへドレインする処理の追加の必要。
- 対象：複数サーバーでの分散が可能なWEBシステムにオススメ。一般的なWEBシステムではロードバランス可能な構成になっていることが多いので、こうした対策を導入するのは非常に容易なハズ

## ③DBサーバーのキャパシティをAutoscalingで可変にする。

![enyasu](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjJ0kd-n3G7vsXVsaJPKjNmLNcQZ4evYO_B2r5Pgwe4qFmc59It7Ek0FSgusJulgT8XRcBAj5D63_zewXkSBQaAqzXQ15I5g0XJ59JAMCoYSd0oZXzAoizw-LNkWkYHPScb9MDT_o171PxyL9nR7ow1_OBVZglGWVS4lP8xPm_rcyK1aFB0HIgOhmew/w585-h323/enyasu-%E3%83%9A%E3%83%BC%E3%82%B83.drawio%20(2).png)

AWSのRDSサービスは利用量に応じた拡張を行う機能（Autoscaling）が存在している。これを利用してDBのキャパシティを固定せず、利用量がひくときはDBのキャパシティを開放することでコストを削減する。

- メリット：RDS利用量のコスト削減が可能。
- デメリット：特になし。あえて言うのであればDB構成変更のための試験が必要なくらい。
- 対象：全システムで導入すべき構成。

## ④DBサーバーのキャパシティをAurolaServlerlessで可変にする。

![enyasu](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh5yq1cruh_xKkFin8u6-zeJWiS4uWgpXKPu-_qm0ReciwHlxAAjDvdqbD5XR3UyYgApUjiVI_cODZaxdX3gziREfib9u4RyajJcxelxXBhtOKzgoM9AI9mctlcUkr28fQGHpsMFvBR02eij8m7ypbOeHO_UBN49wKSxNx4QSYJcxHwo_D5kwLaoL2X/w518-h154/enyasu-%E3%83%9A%E3%83%BC%E3%82%B83%E3%81%AE%E3%82%B3%E3%83%94%E3%83%BC.drawio.png)

AWSのRDSサービスは利用量に応じた拡張を行うサービス、AurolaServerlessが存在している。これを利用してDBのキャパシティを固定せず、利用量がひくときはDBのキャパシティを開放することでコストを削減する。

- メリット：RDS利用量のコスト削減が可能。
- デメリット：特になし。あえて言うのであればDB構成変更のための試験が必要なくらい。
- 対象：全システムで導入すべき構成。

## 結論

他にも様々なサーバー要件に従いコスト削減が可能なパターンがあると思うが、AWSでは工夫次第で様々な方法でコスト削減が可能な構成をとることができる。こうしたタイミングだけでなく、初期設計の段階でもコスト削減を考慮した構成を検討することで、様々なシステムのAWS化を推進することができるだろう。

例）全パターンを混ぜたサーバーコストが1/3程度になる想定の構成

![enyasu](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjdg-Oa5IGlt-p1gYhXI5lIGBGNGVG2CZtUe_KKwpO-XD0ugPrOB_CghtTL8Ze64ZykjjwHCG5c6vdZQvvEVJCF1Ss3akD0_6AOTv7OR4qSYowjZnrDKEGc3majgs35yaGZNbmdkR_Pxw3qVDuFet-i2s2_nKnjgD7cVUuEXWB1bcsY8Cjwn_1NIXu8/w620-h448/enyasu-%E3%83%9A%E3%83%BC%E3%82%B86.drawio.png)
