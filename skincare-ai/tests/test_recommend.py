# test_recommend.py
# ทดสอบ endpoint POST /api/recommend-all ของ SkinCare AI
# รัน: pytest -v --tb=short   (ต้องเปิด backend ที่ 127.0.0.1:5000 ค้างไว้ก่อน)

import pytest, requests
from test_algorithm import TEST_CASES, BASE_URL   # ดึงเคสและ URL จากไฟล์ test_algorithm.py

# เลือกเฉพาะเคสปกติ (ตัด TC4, TC7 ที่เป็น negative ออก) เหลือ TC1, TC2, TC3, TC5, TC6
VALID = [tc for tc in TEST_CASES if not tc.get("negative")]


def post(payload):
    # ฟังก์ชันช่วย: ส่ง request ไป /recommend-all แล้วคืน response (timeout 30 วินาที)
    return requests.post(f"{BASE_URL}/recommend-all", json=payload, timeout=30)


# ─────────────────────────────────────────────────────────────
# เทสต์ 1: ส่งข้อมูลปกติ ระบบต้องตอบสำเร็จและมีสินค้าแนะนำ (ไม่ว่าง)
# รัน 5 รอบ ตามจำนวนเคสใน VALID
# ─────────────────────────────────────────────────────────────
@pytest.mark.parametrize("tc", VALID, ids=lambda t: t["id"])
def test_returns_non_empty_list(tc):
    r = post(tc["payload"])
    assert r.status_code == 200                # ต้องตอบ HTTP 200
    assert len(r.json()["recommend"]) > 0      # รายการ recommend ต้องไม่ว่าง


# ─────────────────────────────────────────────────────────────
# เทสต์ 2: ในรายการแนะนำต้องไม่มีสินค้าซ้ำ (เช็กจาก brand + name)
# xfail: ทราบแล้วว่าเกิดจากข้อมูลในตาราง (BUG-001) ไม่ใช่ engine ส่งซ้ำ
#        ดูรายละเอียดที่ bug-reports/bugs.md
# ─────────────────────────────────────────────────────────────
@pytest.mark.xfail(reason="BUG-001: 117 brand+name groups in products table (data-level)")
@pytest.mark.parametrize("tc", VALID, ids=lambda t: t["id"])
def test_no_duplicate_products(tc):
    items = post(tc["payload"]).json()["recommend"]
    keys = [(p.get("brand"), p.get("name")) for p in items]   # คู่ (แบรนด์, ชื่อ) ของทุกชิ้น
    assert len(keys) == len(set(keys))   # ถ้าไม่ซ้ำ จำนวนทั้งหมดต้องเท่ากับจำนวนที่ไม่ซ้ำ


# ─────────────────────────────────────────────────────────────
# เทสต์ 3: ส่ง input เดิม 2 ครั้ง ผลต้องเหมือนกัน (ระบบต้องคาดเดาได้ ไม่สุ่ม)
# ─────────────────────────────────────────────────────────────
def test_same_input_same_result():
    p = VALID[0]["payload"]                                   # ใช้เคสแรก (TC1)
    a = [x.get("name") for x in post(p).json()["recommend"]]  # ครั้งที่ 1
    b = [x.get("name") for x in post(p).json()["recommend"]]  # ครั้งที่ 2
    assert a == b                                             # รายชื่อและลำดับต้องตรงกัน


# ─────────────────────────────────────────────────────────────
# เทสต์ 4: ส่ง input ผิดรูปแบบ ระบบควรปฏิเสธด้วย 4xx
# (ข้อสมมติของผู้ทดสอบ ถ้าระบบตั้งใจให้ fallback ค่าเริ่มต้น ให้ปรับ Expected)
#   - empty_body          : ส่ง body ว่าง {}
#   - invalid_skin        : skin_type ที่ไม่มีในระบบ
#   - concerns_wrong_type : concerns เป็นข้อความ แทนที่จะเป็น list
# ─────────────────────────────────────────────────────────────

@pytest.mark.xfail(reason="BUG-002: API accepts invalid input with 200 (validation not implemented)")
@pytest.mark.parametrize(
    "bad",
    [{}, {"skin_type": "not_a_type"}, {"skin_type": "oily", "concerns": "acne"}],
    ids=["empty_body", "invalid_skin", "concerns_wrong_type"],
)
def test_invalid_input_is_4xx_not_500(bad):
    assert 400 <= post(bad).status_code < 500   # ต้องเป็น 400–499 (ไม่ใช่ 200 หรือ 500)