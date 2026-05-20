# Lab 2 — Docker Build & Run

**เวลา:** 30 นาที  
**Repository:** `layel2/basic-docker`

---

## วัตถุประสงค์

- ✅ ทำความเข้าใจ Dockerfile แต่ละ instruction
- ✅ ฝึก `docker build`, `docker run`, `docker ps`, `docker logs`
- ✅ ทดสอบ FastAPI ที่รันอยู่ใน Container

---

## ไฟล์ใน Lab นี้

```
lab2-docker/
├── README.md       ← ไฟล์นี้
└── Dockerfile      ← ตัวอย่าง Dockerfile พร้อม comment อธิบาย
```

> **หมายเหตุ:** Dockerfile จริงที่ใช้ build อยู่ที่ root ของ repo (`../Dockerfile`)

---

## Dockerfile อธิบาย

```dockerfile
# 1. Base Image — ใช้ Python 3.11 แบบ slim (ขนาดเล็ก)
FROM python:3.11-slim

# 2. Copy requirements ก่อน (ใช้ Docker layer cache ให้เป็นประโยชน์)
ADD ./requirements.txt /app/requirements.txt

# 3. ตั้ง working directory
WORKDIR /app

# 4. ติดตั้ง dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 5. Copy source code
ADD ./src/ /app/

# 6. เปิด port สำหรับ FastAPI
EXPOSE 8000

# 7. คำสั่งเริ่ม server
CMD ["uvicorn", "main:app", "--port", "8000", "--reload"]
```

---

## ขั้นตอน

### 1. Clone และเข้า directory

```bash
git clone https://github.com/layel2/basic-docker.git
cd basic-docker
```

### 2. ดู Dockerfile

```bash
cat Dockerfile
cat requirements.txt
```

### 3. Build Docker Image

```bash
# -t = tag (ตั้งชื่อ image)
# .  = บอกว่า Dockerfile อยู่ที่ current directory
docker build -t testapi .

# ดู image ที่ build แล้ว
docker images
```

### 4. Run Container

```bash
# -d         = detach (background)
# -p 8000:8000 = map port host:container
# --name     = ตั้งชื่อ container
docker run -d -p 8000:8000 --name my-api testapi

# ตรวจสอบว่ารันอยู่
docker ps
```

### 5. ทดสอบ API

```bash
curl http://localhost:8000
# {"message":"Hello world","status":true}

curl http://localhost:8000/health
# {"status":"healthy","version":"1.0.0"}

curl http://localhost:8000/hello/pranpaveen
# {"message":"Hello, pranpaveen!","name":"pranpaveen"}

curl http://localhost:8000/items
# {"items":[...],"total":3}
```

เปิด Swagger UI: http://localhost:8000/docs

### 6. ดู Logs

```bash
docker logs my-api          # ดู logs ทั้งหมด
docker logs -f my-api       # ดู live logs (Ctrl+C เพื่อออก)
```

### 7. Run Tests ใน Container

```bash
docker run testapi pytest -v
# ควรเห็น: 21 passed
```

### 8. Cleanup

```bash
docker stop my-api
docker rm my-api
docker ps -a    # ตรวจสอบว่าไม่มีแล้ว
```

