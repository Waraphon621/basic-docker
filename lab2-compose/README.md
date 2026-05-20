# Lab 2b — Docker Compose

**เวลา:** 20 นาที  
**Repository:** `layel2/basic-docker`

---

## วัตถุประสงค์

- ✅ เขียนและทำความเข้าใจ `docker-compose.yml`
- ✅ รัน multi-container app ด้วยคำสั่งเดียว
- ✅ ทำความเข้าใจ volumes และ environment variables

---

## ไฟล์ใน Lab นี้

```
lab2b-compose/
├── README.md            ← ไฟล์นี้
└── docker-compose.yml   ← ตัวอย่างพร้อม comment
```

> **หมายเหตุ:** `docker-compose.yml` จริงอยู่ที่ root ของ repo (`../docker-compose.yml`)

---

## docker-compose.yml อธิบาย

```yaml
version: '3.8'

services:

  app:                          # Service ที่ 1: FastAPI app
    build: .                    # build จาก Dockerfile ที่ root
    container_name: fastapi-app
    ports:
      - "8000:8000"             # host:container
    environment:
      - APP_ENV=development     # env var ที่ส่งเข้า container
      - APP_VERSION=1.0.0
    volumes:
      - ./src:/app              # bind mount — hot reload
    depends_on:
      - redis                   # รอ redis พร้อมก่อน start
    restart: unless-stopped

  redis:                        # Service ที่ 2: Redis cache
    image: redis:7-alpine       # ใช้ official image
    container_name: redis-cache
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data        # named volume — ข้อมูล persist

volumes:
  redis_data:                   # Docker จัดการ path ให้อัตโนมัติ
```

---

## ขั้นตอน

### 1. เริ่ม Services ทั้งหมด

```bash
# จาก root ของ repo
docker compose up -d

# ดูสถานะ
docker compose ps
```

### 2. ทดสอบ App

```bash
curl http://localhost:8000
curl http://localhost:8000/health

# ดู Swagger UI
# เปิด browser: http://localhost:8000/docs
```

### 3. ดู Logs

```bash
docker compose logs             # ทุก service
docker compose logs app         # เฉพาะ app
docker compose logs -f app      # live logs
```

### 4. ทดสอบ Volume (Hot Reload)

แก้ไขโค้ดใน `src/main.py` — เช่น เปลี่ยน message ใน `GET /`  
แล้วเรียก API อีกครั้ง โดยไม่ต้อง restart container

```bash
# ทดสอบ
curl http://localhost:8000
# ควรเห็น message ที่เปลี่ยนแปลงทันที
```

### 5. ดู Environment Variables ใน Container

```bash
docker compose exec app env | grep APP
# APP_ENV=development
# APP_VERSION=1.0.0
```

### 6. Cleanup

```bash
docker compose down           # หยุด + ลบ containers และ networks
docker compose down -v        # ลบ volumes ด้วย (ข้อมูล redis หาย)
docker compose ps             # ตรวจสอบ
```

