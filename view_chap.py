import json
import os
from collections import defaultdict

# 경로 설정
image_base_path = "images"
chapter_folder = "chapters"
os.makedirs(chapter_folder, exist_ok=True)

# JSON 로드
with open("NAPD_frag_trans4.1_postprocessed.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 챕터별 분류
chapters = defaultdict(list)
chapter_titles = {}

for item in data:
    chap_id_full = item.get("chapter_id", "").strip()
    if not chap_id_full:
        continue

    chap_num = chap_id_full.split('-')[0]

    if chap_id_full.endswith("-0"):
        chapter_titles[chap_num] = item["trans"].strip().split("\n")[0]

    chapters[chap_num].append(item)

# 챕터 번호 정렬
sorted_chaps = sorted(
    (k for k in chapters.keys() if k != "0"), key=lambda x: int(x)
)

# ✅ 목차 HTML 생성
toc_html = """
<html>
<head><meta charset='utf-8'>
<style>
  body { font-family: sans-serif; font-size: 17px; line-height: 1.8; margin: 40px 5%; }
  ul { list-style-type: none; padding: 0; }
  li { margin: 0.5em 0; }
</style>
</head>
<body>
<h1>📚 Nutrition and Physical Degeneration</h1>
<ul>
"""

for chap_num in sorted_chaps:
    title = chapter_titles.get(chap_num, f"Chapter {chap_num}")
    toc_html += f"<li><a href='{chapter_folder}/chapter-{chap_num.zfill(2)}.html'>{title}</a></li>\n"

toc_html += "</ul></body></html>"

with open("view_chapters.html", "w", encoding="utf-8") as f:
    f.write(toc_html)

# ✅ 각 챕터 HTML 생성
for idx, chap_num in enumerate(sorted_chaps):
    content_html = ""

    for item in chapters[chap_num]:
        chap_id_full = item.get("chapter_id", "").strip()
        if item["type"] == "text":
            if chap_id_full.endswith("-0"):
                content_html += f"<h2 class='chapter-title'>{item['trans'].replace(chr(10), '<br>')}</h2>\n"
            elif chap_id_full.endswith("-1"):
                content_html += f"<h3 class='section-title'>{item['trans'].replace(chr(10), '<br>')}</h3>\n"
            else:
                content_html += f"<div class='paragraph'><p>{item['trans'].replace(chr(10), '<br>')}</p></div>\n"
        elif item["type"] == "image":
            image_filename = item["filename"]
            image_path = os.path.join(image_base_path, image_filename)
            if os.path.exists(image_path):
                rel_path = f"../{image_base_path}/{image_filename}"
                content_html += f"<div><img src='{rel_path}' alt='{image_filename}'></div>\n"
            else:
                content_html += f"<div><p>[이미지 누락: {image_filename}]</p></div>\n"

    # 하단 내비게이션
    nav_html = "<hr><div style='margin-top:30px;'>"
    if idx > 0:
        prev_chap = sorted_chaps[idx - 1]
        prev_title = chapter_titles.get(prev_chap, f"Chapter {prev_chap}")
        nav_html += f"<a href='chapter-{prev_chap.zfill(2)}.html'>← {prev_title}</a>"

    nav_html += f" | <a href='../view_chapters.html'>📘 목차로</a>"

    if idx < len(sorted_chaps) - 1:
        next_chap = sorted_chaps[idx + 1]
        next_title = chapter_titles.get(next_chap, f"Chapter {next_chap}")
        nav_html += f" | <a href='chapter-{next_chap.zfill(2)}.html'>{next_title} →</a>"

    nav_html += "</div>"

    # 최종 HTML
    chapter_html = f"""
    <html>
    <head><meta charset='utf-8'>
    <style>
      body {{ font-family: sans-serif; font-size: 17px; line-height: 1.8; margin: 40px 20%; }}
      h2.chapter-title {{ font-size: 28px; font-weight: bold; margin-top: 60px; }}
      h3.section-title {{ font-size: 22px; font-weight: bold; margin-top: 40px; }}
      .paragraph {{ margin-bottom: 24px; }}
      img {{ max-width: 100%; margin: 20px 0; }}
    </style>
    </head>
    <body>
    <a href="../view_chapters.html">← 목차로 돌아가기</a>
    {content_html}
    {nav_html}
    </body>
    </html>
    """

    # 챕터별 파일 저장
    with open(os.path.join(chapter_folder, f"chapter-{chap_num.zfill(2)}.html"), "w", encoding="utf-8") as f:
        f.write(chapter_html)
