---
layout: default
title: ホーム
---
GitHub Pages + Jekyll で作ったブログです。
技術メモや日々の記録を書いていきます。

## 最新の記事
<ul class="post-list">
  {% for post in site.posts %}
    <li class="post-item">
      <a class="post-title" href="{{ post.url }}">{{ post.title }}</a>
      <span class="post-date">{{ post.date | date: "%Y-%m-%d" }}</span>
      {% if post.excerpt %}
        <p class="post-excerpt">{{ post.excerpt }}</p>
      {% endif %}
    </li>
  {% endfor %}
</ul>
