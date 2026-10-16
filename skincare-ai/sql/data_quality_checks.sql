-- data_quality_checks.sql — ตรวจคุณภาพข้อมูลตาราง products (อ่านอย่างเดียว ไม่แก้ข้อมูล)

-- 1) สรุปภาพรวม
SELECT '1 แถวทั้งหมด' AS check_name, COUNT(*)::text AS result FROM products
UNION ALL
SELECT '2 กลุ่ม brand+name ที่มีมากกว่า 1 แถว', COUNT(*)::text
FROM (SELECT 1 FROM products GROUP BY brand, name HAVING COUNT(*) > 1) t
UNION ALL
SELECT '3 คู่ brand+name เดียวกัน ส่วนผสมเหมือนกัน', COUNT(*)::text
FROM products a JOIN products b ON a.brand = b.brand AND a.name = b.name AND a.id < b.id
WHERE a.ingredients_list = b.ingredients_list
UNION ALL
SELECT '4 คู่ brand+name เดียวกัน ส่วนผสมต่างกัน', COUNT(*)::text
FROM products a JOIN products b ON a.brand = b.brand AND a.name = b.name AND a.id < b.id
WHERE a.ingredients_list IS DISTINCT FROM b.ingredients_list
UNION ALL
SELECT '5 product_url ที่ซ้ำกัน', COUNT(*)::text
FROM (SELECT 1 FROM products GROUP BY product_url HAVING COUNT(*) > 1) t;

-- 2) index ของตาราง (ตรวจว่ามี unique บน product_url หรือไม่)
SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'products';

-- 3) กลุ่ม brand+name ที่ซ้ำ (urls = จำนวน URL ที่ต่างกัน)
SELECT brand, name, COUNT(*) AS n, COUNT(DISTINCT product_url) AS urls
FROM products GROUP BY brand, name HAVING COUNT(*) > 1
ORDER BY n DESC, brand LIMIT 30;