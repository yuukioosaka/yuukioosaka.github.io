---
layout: default
title: ホーム
---
# @yukiosak1-長文-
GitHub Pages + Jekyll で作ったブログです。
技術メモや日々の記録を書いていきます。

## 最新の記事
<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a> — {{ post.date | date: "%Y-%m-%d" }}
    </li>
  {% endfor %}
</ul>
