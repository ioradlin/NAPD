import json

file_path = "/home/sonhyelin/data/NAPD/NAPD_frag_trans4.1_postprocessed.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# "이다"로 끝나는 trans를 수정
for item in data:
    if isinstance(item, dict):
        trans = item.get("trans", "").strip()
        if trans.endswith("이다"):
            print(item["trans"])
            #item["trans"] = trans[:-2]  # "이다" 제거 후 공백도 정리
        if " 도 " in trans:
            idx = trans.index(" 도 ")
            print("전:" , trans[idx:idx+10])
            trans= trans.replace(" 도 ", " 그림 ")
            print(trans[idx:idx+10])
            item["trans"] = trans

# 결과를 다시 같은 파일에 저장
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
