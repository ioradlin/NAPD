import json

with open("NAPD_frag_trans2_finished.json", "r", encoding="utf-8") as f:
    data = json.load(f)

id = 0
sub_id = 0

for i, item in enumerate(data):
    if item["type"] != "text":
        item["chapter_id"] = str(id)+'-'+"img"
        continue
    if item["text"].startswith("Chapter "):
        id += 1
        sub_id = 0
    else:
        sub_id += 1
    item["chapter_id"] = str(id)+'-'+str(sub_id)

    item["text"] = item["text"].replace("\n", " ").strip()
        
with open("NAPD_frag_trans2_postprocessed.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)