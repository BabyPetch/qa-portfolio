# Testing SkinCare AI

ชุดทดสอบสำหรับระบบแนะนำผลิตภัณฑ์สกินแคร์ SkinCare AI (React + Flask + scikit-learn + PostgreSQL)
ตัวระบบพัฒนาเป็นทีม 2 คน ดูโค้ดได้ที่ [ใส่ลิงก์ repo SkinCare AI](https://github.com/BabyPetch/[ชื่อ-repo-skincare])
เทสต์ทั้งหมดในโฟลเดอร์นี้เขียนแบบ black-box คือทดสอบผ่าน URL จากภายนอก ไม่แก้โค้ดของระบบ

## สิ่งที่ทดสอบ
- **Algorithm / API:** `POST /api/recommend-all` ผลแนะนำตรงกับผิวและปัญหาที่เลือก, กรณี input ผิดปกติ (negative, edge case)
- **คุณภาพผลลัพธ์:** ผลไม่ซ้ำ, input เดิมได้ผลเดิม, input ผิดรูปแบบต้องได้ 4xx ไม่ใช่ 500
- **ฟอร์ม 9 ขั้น และสิทธิ์ Admin/User/Guest:** ทดสอบด้วยมือตาม test case
- **API เพิ่มเติม:** Postman collection

## โครงสร้าง
| โฟลเดอร์ | เนื้อหา |
|---|---|
| `tests/` | `test_algorithm.py` (7 เคส พร้อมรายงานเป็นตาราง), `test_recommend.py` (pytest) |
| `test-cases/` | Test case [N] ข้อ พร้อมผล Actual/Status |
| `postman/` | Postman collection |
| `bug-reports/` | บั๊กที่พบ |

## วิธีรัน
1. รัน SkinCare AI ในเครื่อง ตามขั้นตอนใน repo ของระบบ (backend ที่ `http://127.0.0.1:5000`, frontend ที่ `http://localhost:5173`)
2. ติดตั้งไลบรารีทดสอบ
```bash
   pip install pytest requests tabulate
```
3. รันเทสต์
```bash
   cd skincare-ai/tests
   pytest -v          # เทสต์อัตโนมัติ
   python test_algorithm.py   # รายงานเปรียบเทียบผลแบบตาราง
```

## ผลที่ได้ (เติมหลังรันจริง)
- pytest: [X] passed, [Y] failed (จาก [N] เทสต์)
- Test case ทดสอบมือ: [N] ข้อ, ผ่าน [X], ไม่ผ่าน [Y]
- บั๊กที่พบ: [N] รายการ ดู [bug-reports/bugs.md](bug-reports/bugs.md)

## ข้อจำกัด
- ต้องรันระบบในเครื่องก่อน เทสต์ทำงานกับ `localhost`
- เกณฑ์ตัดสินผลแนะนำในบางเคสใช้ keyword และประเภทผิวเป็นตัวตรวจ ซึ่งยังเป็นแบบหยาบ