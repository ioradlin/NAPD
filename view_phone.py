import json
import os
from collections import defaultdict

# 경로 설정
image_base_path = "images"
chapter_folder = "chapters_phone"  # 변경된 폴더명
os.makedirs(chapter_folder, exist_ok=True)

with open("NAPD_frag_trans4.1_postprocessed.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def get_filename(chap_num):
    return special_chapters[chap_num]["filename"] if chap_num in special_chapters else f"chapter-{chap_num.zfill(2)}.html"


# 챕터 분류
docs_by_chapter = defaultdict(list)
chapter_titles = {}

# # 1. 특수 챕터 정의
special_chapters = {
    "s00": {
        "title_id": "0-1",
        "content_ids": ["0-2", "0-3"],
        "filename": "chapter-s00.html",
        "chaptername": "chapter-s00.html"
    },
    "s02": {
        "title_id": "0-13",
        "content_ids": [f"0-{i}" for i in range(14, 20)],
        "filename": "chapter-s02.html",
        "chaptername": "chapter-s02.html"
    },
    "s01": {
        "title_id": "0-7",
        "content_ids": ["0-8"],
        "filename": "chapter-s01.html",
        "chaptername": "chapter-s01.html"
    }
    
}


# 특수챕터 생성
for chap_key, info in special_chapters.items():
    title_item = next((item for item in data if item.get("chapter_id") == info["title_id"]), None)
    content_items = [item for item in data if item.get("chapter_id") in info["content_ids"]]

    print("---")
    print(title_item)
    #print(content_items)
    if not title_item:
        continue  # title이 없으면 건너뜀

    html = f"""
    <html>
    <head>
      <meta charset='utf-8'>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <style>
        body {{ font-family: sans-serif; font-size: 17px; line-height: 1.8; margin: 40px auto; max-width: 720px; padding: 0 16px; }}
        h2.chapter-title {{ font-size: 28px; font-weight: bold; margin-top: 60px; }}
        .paragraph {{ margin-bottom: 24px; }}
        img {{ max-width: 100%; height: auto; margin: 20px 0; }}
      </style>
    </head>
    <body>
    <a href="../view_phone.html">← 목차로 돌아가기</a>
    <h2 class='chapter-title'>{title_item['trans'].replace(chr(10), '<br>')}</h2>
    """

    #print(title_item['trans'].replace(chr(10), '<br>'))

    for item in content_items:
        if item["type"] == "text":
            html += f"<div class='paragraph'><p>{item['trans'].replace(chr(10), '<br>')}</p></div>\n"
        elif item["type"] == "image":
            image_filename = item["filename"]
            rel_path = f"{image_base_path}/{image_filename}"
            html += f"<div><img src='{rel_path}' alt='{image_filename}'></div>\n"

    html += "</body></html>"

    with open(os.path.join(chapter_folder, info["filename"]), "w", encoding="utf-8") as f:
        f.write(html)
        

    # 목차용 정보 추가
    chapter_titles[chap_key] = title_item["trans"].split("\n")[0]
    docs_by_chapter[chap_key] = []  # 내용은 없어도 chap_num 확보를 위해

print(chapter_titles)
print(docs_by_chapter)





for item in data:
    chap_id_full = item.get("chapter_id")
    if not chap_id_full:
        continue

    chap_num = chap_id_full.split('-')[0]
    if chap_num == "0":
        continue

    if chap_id_full.endswith("-0"):
        chapter_titles[chap_num] = item["trans"].strip().split("\n")[0]

    docs_by_chapter[chap_num].append(item)
    if chap_id_full.startswith('0'):
        print(chap_id_full)

# 정렬
special_order = ["s00", "s01", "s02"]
rest_chaps = sorted([k for k in docs_by_chapter if k not in special_order and k != "0"], key=int)
sorted_chaps = special_order + rest_chaps
#print(sorted_chaps)

# 목차 페이지 생성 (view_phone.html)
toc_html = """
<html>
<head>
  <meta charset='utf-8'>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body { font-family: sans-serif; font-size: 17px; line-height: 1.8; margin: 40px auto; max-width: 720px; padding: 0 16px; }
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

    if chap_num in special_chapters:
        filename = f"{chapter_folder}/{special_chapters[chap_num]['chaptername']}"
        print(filename)
    else:
        filename = f"{chapter_folder}/chapter-{chap_num.zfill(2)}.html"
        

    toc_html += f"<li><a href='{filename}'>{title}</a></li>\n"
    print(toc_html)


toc_html += "</ul></body></html>"

with open("view_phone.html", "w", encoding="utf-8") as f:
    f.write(toc_html)

# 챕터 HTML 생성
for idx, chap_num in enumerate(sorted_chaps):
    if not docs_by_chapter[chap_num]: #special chapters.
        continue

    content_html = ""

    for item in docs_by_chapter[chap_num]:
        chap_id_full = item.get("chapter_id", "")

        if item["type"] == "text":
            if chap_id_full.endswith("-0"):
                content_html += f"<h2 class='chapter-title'>{item['trans'].replace(chr(10), '<br>')}</h2>\n"
            elif chap_id_full.endswith("-1"):
                content_html += f"<h3 class='section-title'>{item['trans'].replace(chr(10), '<br>')}</h3>\n"
            else:
                content_html += f"<div class='paragraph'><p>&nbsp;{item['trans'].replace(chr(10), '<br>')}</p></div>\n"

        elif item["type"] == "image":
            image_filename = item["filename"]
            image_path = os.path.join(image_base_path, image_filename)
            if os.path.exists(image_path):
                rel_path = f"../{image_base_path}/{image_filename}"
                content_html += f"<div><img src='{rel_path}' alt='{image_filename}'></div>\n"
            else:
                content_html += f"<div><p>[이미지 누락: {image_filename}]</p></div>\n"

    nav_html = "<hr><div style='margin-top:30px;'>"

    if idx > 0:
        prev_chap = sorted_chaps[idx - 1]
        prev_title = chapter_titles.get(prev_chap, f"Chapter {prev_chap}")
        nav_html += f"<a href='{get_filename(prev_chap)}'>← {prev_title}</a>"

    nav_html += f" | <a href='../view_phone.html'>📘 목차로</a>"

    if idx < len(sorted_chaps) - 1:
        next_chap = sorted_chaps[idx + 1]
        next_title = chapter_titles.get(next_chap, f"Chapter {next_chap}")
        nav_html += f" | <a href='{get_filename(next_chap)}'>{next_title} →</a>"

    nav_html += "</div>"

    chapter_html = f"""
    <html>
    <head>
      <meta charset='utf-8'>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <style>
        body {{ font-family: sans-serif; font-size: 17px; line-height: 1.8; margin: 40px auto; max-width: 720px; padding: 0 16px; }}
        h2.chapter-title {{ font-size: 28px; font-weight: bold; margin-top: 60px; }}
        h3.section-title {{ font-size: 22px; font-weight: bold; margin-top: 40px; }}
        .paragraph {{ margin-bottom: 24px; }}
        img {{ max-width: 100%; height: auto; margin: 20px 0; }}
      </style>
    </head>
    <body>
    <a href="../view_phone.html">← 목차로 돌아가기</a>
    {content_html}
    {nav_html}
    </body>
    </html>
    """

    with open(os.path.join(chapter_folder, f"chapter-{chap_num.zfill(2)}.html"), "w", encoding="utf-8") as f:
        f.write(chapter_html)

