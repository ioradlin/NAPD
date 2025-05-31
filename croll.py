import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import json

# 1. URL 설정 및 HTML 요청
url = "https://gutenberg.net.au/ebooks02/0200251h.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# 2. 이미지 저장 폴더 생성
os.makedirs("images", exist_ok=True)

# 3. <p>와 <img>를 순서대로 읽기
elements = soup.body.find_all(["p", "img"], recursive=True)

structured = []
para_id = 1

for el in elements:
    if el.name == "p":
        text = el.get_text(strip=True)
        if text:
            structured.append({
                "type": "text",
                "para_id": f"{para_id:04d}",
                "text": text
            })
            para_id += 1
    elif el.name == "img":
        src = el.get("src")
        if not src:
            continue

        # 절대 URL 구성
        img_url = urljoin(url, src)
        filename = src.split("/")[-1]  # 예: "0200251h-images/Fig.1.jpg" → "Fig.1.jpg"
        local_path = os.path.join("images", filename)

        # 이미지 저장
        try:
            img_data = requests.get(img_url).content
            with open(local_path, "wb") as f:
                f.write(img_data)
            print(f"✔ Saved image: {local_path}")
        except Exception as e:
            print(f"✘ Failed to download {img_url}: {e}")

        # 구조에 추가
        structured.append({
            "type": "image",
            "src": src,
            "filename": filename
        })

# 4. 저장
with open("structured_with_images.json", "w", encoding="utf-8") as f:
    json.dump(structured, f, indent=2, ensure_ascii=False)

print("✅ 모든 문단 및 이미지 정보를 structured_with_images.json에 저장 완료.")
