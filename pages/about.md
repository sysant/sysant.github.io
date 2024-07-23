---
layout: page
title: About
description: 打码改变世界
keywords: sysnat, san, yongc_dong 
comments: true
menu: 关于
permalink: /about/
---

学习如春之禾苗，不见所增日有所长！


## 联系

<ul>
{% for website in site.data.social %}
<li>{{website.sitename }}：<a href="{{ website.url }}" target="_blank">@{{ website.name }}</a></li>
{% endfor %}
{% if site.url contains 'http://47.121.194.76:10800/' %}
{% endif %}
</ul>


## Skill Keywords

{% for skill in site.data.skills %}
### {{ skill.name }}
<div class="btn-inline">
{% for keyword in skill.keywords %}
<button class="btn btn-outline" type="button">{{ keyword }}</button>
{% endfor %}
</div>
{% endfor %}
