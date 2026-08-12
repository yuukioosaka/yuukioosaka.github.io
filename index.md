---
layout: default
title: yukiosakのブログ
---
GitHub Pages + Jekyll で作ったブログです。
市場分析、技術メモ、日々の記録を主にAIが書いていきます。

## 最新の記事
<ul class="post-list">
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">
        <strong>{{ post.title }}</strong>
        <span class="post-date">{{ post.date | date: "%Y-%m-%d" }}</span>
      </a>
      {% if post.excerpt %}
        <p>{{ post.excerpt }}</p>
      {% endif %}
    </li>
  {% endfor %}
</ul>
