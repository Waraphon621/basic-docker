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
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
