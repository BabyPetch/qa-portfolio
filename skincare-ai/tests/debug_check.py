import requests, collections
from test_algorithm import TEST_CASES, BASE_URL

# 1) ดูสินค้าซ้ำ
payload = TEST_CASES[0]["payload"]
items = requests.post(f"{BASE_URL}/recommend-all", json=payload, timeout=30).json()["recommend"]
print("fields:", list(items[0].keys()))
groups = collections.defaultdict(list)
for p in items:
    groups[(p.get("brand"), p.get("name"))].append(p)
for key, ps in groups.items():
    if len(ps) > 1:
        print(key)
        for p in ps:
            print("   ", {k: p.get(k) for k in ("id", "product_id", "price", "skintype", "final_score") if k in p})

# 2) ดูว่า input ผิดได้ผลอะไรกลับมา
for name, bad in [("empty", {}), ("bad_skin", {"skin_type": "not_a_type"}), ("concerns_str", {"skin_type": "oily", "concerns": "acne"})]:
    r = requests.post(f"{BASE_URL}/recommend-all", json=bad, timeout=30)
    d = r.json()
    print(name, r.status_code, list(d.keys()), len(d.get("recommend", [])))