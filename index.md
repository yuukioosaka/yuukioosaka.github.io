---
layout: default
title: ホーム
---
GitHub Pages + Jekyll で作ったブログです。
技術メモや日々の記録を書いていきます。

## 最新の記事
<ul class="post-list list-style-none pl-0">
  {% for post in site.posts %}
    <a class="post-card border box-shadow-medium rounded-2 p-3 mb-3 no-underline" href="{{ post.url }}">
      <div class="d-flex flex-justify-between flex-items-baseline">
        <h3 class="post-title h4 mt-0 mb-0 flex-auto">{{ post.title }}</h3>
        <span class="f6 text-gray-light no-wrap ml-3">{{ post.date | date: "%Y-%m-%d" }}</span>
      </div>
      {% if post.excerpt %}
        <p class="post-excerpt text-gray mt-2 mb-0">{{ post.excerpt }}</p>
      {% endif %}
    </a>
  {% endfor %}
</ul>
