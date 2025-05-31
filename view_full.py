import json
import os
import re

image_base_path = "images"

with open("NAPD_frag_trans4.1_postprocessed.json", "r", encoding="utf-8") as f:
    data = json.load(f)

html_output = """
<html>
<head>
  <meta charset='utf-8'>
  <style>
    body { font-family: sans-serif; line-height: 1.6; margin: 40px; }
    .paragraph { margin-bottom: 24px; }
    img { max-width: 100%; margin: 20px 0; }
    .toc { background: #f0f0f0; padding: 10px; border: 1px solid #ccc; }
  </style>
</head>
<body>
<a id="top"></a>
<h1>📚 목차</h1>
<div class="toc">
<ul>
"""

# 1. TOC 만들기
chapters = []
chapter_ids = []
chapter_count = 0

for item in data:
    if item["type"] == "text" and re.match(r"Chapter\s+\d+", item["text"]):
        chapter_count += 1
        chapter_title = item["trans"]
        chapter_id = f"chapter-{chapter_count}"
        chapters.append((chapter_id, chapter_title))
        chapter_ids.append(item["para_id"])
        html_output += f"<li><a href='#{chapter_id}'>{chapter_title}</a></li>"

html_output += "</ul></div><hr>\n"

# 2. 본문 출력
current_chapter = None

for item in data:
    if item["type"] == "text" and re.match(r"Chapter\s+\d+", item["text"]):
        # 새 챕터 시작
        current_chapter = chapter_ids.pop(0)
        chapter_anchor = f"chapter-{len(chapters) - len(chapter_ids)}"
        html_output += f"<h2 id='{chapter_anchor}'>{item['trans']}</h2>\n"
    elif item["type"] == "text":
        html_output += f"<div class='paragraph'><p>{item['trans'].replace(chr(10), '<br>')}</p></div>\n"
    elif item["type"] == "image":
        image_filename = item["filename"]
        image_path = os.path.join(image_base_path, image_filename)
        if os.path.exists(image_path):
            rel_path = f"{image_base_path}/{image_filename}"
            html_output += f"<div><img src='{rel_path}' alt='{image_filename}'></div>\n"
        else:
            html_output += f"<div><p>[이미지 누락: {image_filename}]</p></div>\n"

html_output += "</body></html>"

with open("output.html", "w", encoding="utf-8") as f:
    f.write(html_output)
