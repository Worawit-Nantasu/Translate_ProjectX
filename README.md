# JSON Translation Tool

โปรเจ็คนี้เป็นเครื่องมือสำหรับการแปลไฟล์ JSON จากภาษาหนึ่งไปยังอีกภาษาหนึ่งโดยอัตโนมัติ โดยใช้ไลบรารี [deep_translator](https://github.com/nidhaloff/deep-translator) (GoogleTranslator) พร้อมทั้งการกำหนดค่าภาษาต้นทางและภาษาปลายทาง และการกำหนดคีย์ที่ไม่ต้องแปล

## คุณสมบัติเด่น

- **แปลไฟล์ JSON หลายไฟล์พร้อมกัน:**  
  ใช้ ThreadPoolExecutor ในการแปลไฟล์แบบขนาน เพิ่มความเร็วในการประมวลผลหากมีไฟล์หลายไฟล์
- **รองรับการนับสตริง:**  
  มีฟังก์ชันนับจำนวนสตริงที่ต้องแปลและแสดงแถบความคืบหน้าด้วย `tqdm`
- **Cache การแปล:**  
  ลดการแปลข้อความซ้ำ ๆ โดยเก็บผลลัพธ์ไว้ใน cache
- **ตั้งค่าภาษา และคีย์ที่ไม่ต้องแปล:**  
  กำหนดภาษาแหล่งที่มา (SOURCE_LANG) และภาษาปลายทาง (TARGET_LANG) ในไฟล์ `config/settings.py` พร้อมทั้งกำหนดคีย์ที่ไม่ต้องแปล (DO_NOT_TRANSLATE_KEYS)

## โครงสร้างโปรเจ็ค

```
.
├── README.md
├── config
│   └── settings.py           # กำหนด SOURCE_LANG, TARGET_LANG และ DO_NOT_TRANSLATE_KEYS
├── data
│   ├── input                 # ไฟล์ JSON ต้นฉบับที่ต้องการแปล
│   └── output                # ไฟล์ JSON ที่แปลเสร็จจะถูกบันทึกที่นี่
├── logs
│   └── translation.log       # ไฟล์ log บันทึกเหตุการณ์การแปล
├── scripts
│   ├── __init__.py
│   ├── translate_json.py     # สคริปต์หลักสำหรับการแปลหลายไฟล์พร้อมกัน
│   └── utils.py              # ฟังก์ชันช่วยเหลือในการแปล
├── tests
│   └── test_translation.py   # ไฟล์ทดสอบ (หากมี)
└── venv                      # Python Virtual Environment (optional)
```

## ขั้นตอนการติดตั้งและใช้งาน

### 1. ติดตั้ง Python Virtual Environment (แนะนำ)

```bash
python3 -m venv venv
source venv/bin/activate  # บน Linux/Mac
venv\Scripts\activate      # บน Windows
```

### 2. ติดตั้ง dependencies

โปรดตรวจสอบว่ามีไฟล์ `requirements.txt` หรือไม่ หากมี ให้รัน:

```bash
pip install -r requirements.txt
```

หากยังไม่ได้ติดตั้ง `deep_translator` หรือ `tqdm` สามารถติดตั้งด้วยคำสั่ง:

```bash
pip install deep-translator tqdm
```

### 3. กำหนดค่าภาษาต้นทางและภาษาปลายทาง

ในไฟล์ `config/settings.py` ปรับค่า:

```python
SOURCE_LANG = 'fr'  # ภาษาต้นทาง เช่น ภาษาฝรั่งเศส
TARGET_LANG = 'th'  # ภาษาปลายทาง เช่น ภาษาไทย
```

ปรับรายการ `DO_NOT_TRANSLATE_KEYS` ตามต้องการ

### 4. วางไฟล์ JSON ต้นฉบับใน `data/input`

นำไฟล์ `.json` ที่ต้องการแปลไปใส่ใน `data/input`

### 5. รันสคริปต์แปล

```bash
python scripts/translate_json.py
```

โปรแกรมจะ:

- สแกนไฟล์ `.json` ใน `data/input`
- แปลไฟล์แต่ละไฟล์พร้อมแสดงความคืบหน้าด้วย `tqdm`
- ไฟล์ที่แปลแล้วจะถูกบันทึกใน `data/output` ด้วยชื่อไฟล์เดิม

### 6. ตรวจสอบบันทึกการทำงาน

ดูไฟล์ `logs/translation.log` เพื่อดูข้อมูลการทำงาน การแจ้งเตือน หรือข้อผิดพลาด

## การทดสอบ

หากมีการเขียนเทสไว้ใน `tests/test_translation.py` สามารถรันการทดสอบด้วย:

```bash
pytest tests
```

(อาจต้องติดตั้ง `pytest` ก่อนด้วย `pip install pytest`)

## คำแนะนำเพิ่มเติม

- หากโครงสร้างของ JSON ซับซ้อน ควรทดสอบกับไฟล์ขนาดเล็กก่อน
- ตรวจสอบให้แน่ใจว่าระบบอินเทอร์เน็ตเชื่อมต่อและ GoogleTranslator สามารถทำงานได้
- สามารถปรับจำนวน `max_workers` ใน ThreadPoolExecutor ที่ `translate_multiple_files` ตามสมรรถนะของเครื่อง
