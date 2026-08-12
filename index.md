---
layout: default
title: ホーム
---
GitHub Pages + Jekyll で作ったブログです。
技術メモや日々の記録を書いていきます。

## 最新の記事
<ul class="post-list">
  {% for post in site.posts %}
    <a href="{{ post.url }}">
      <div class="d-flex flex-justify-between flex-items-baseline">
        <h3 class="h4 mt-0 mb-0 flex-auto">{{ post.title }}</h3>
        <span class="f6 text-gray-light no-wrap ml-3">{{ post.date | date: "%Y-%m-%d" }}</span>
      </div>
      {% if post.excerpt %}
        <p>{{ post.excerpt }}</p>
      {% endif %}
    </a>
  {% endfor %}
</ul>
