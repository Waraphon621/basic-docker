from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Basic Docker API",
    description="FastAPI demo สำหรับสอน Docker & Docker Compose",
    version="1.0.0",
)

# ── In-memory storage (สำหรับ demo) ──────────────────────────────────────────
items_db: dict[int, dict] = {
    1: {"id": 1, "name": "Laptop",  "price": 35000, "in_stock": True},
    2: {"id": 2, "name": "Mouse",   "price": 450,   "in_stock": True},
    3: {"id": 3, "name": "Keyboard","price": 1200,  "in_stock": False},
}
next_id = 4


# ── Request model ─────────────────────────────────────────────────────────────
class ItemCreate(BaseModel):
    name: str
    price: float
    in_stock: Optional[bool] = True


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/", tags=["home"])
async def home() -> dict:
    """Root endpoint — ทดสอบว่า API ทำงานอยู่"""
    return {"message": "Hello world", "status": True}


@app.get("/health", tags=["home"])
async def health() -> dict:
    """Health check — ใช้ใน CI/CD และ container orchestration"""
    return {"status": "healthy", "version": app.version}


@app.get("/hello/{name}", tags=["greeting"])
async def hello(name: str) -> dict:
    """ทักทายแบบ personalized — ตัวอย่าง path parameter"""
    if not name.strip():
        raise HTTPException(status_code=400, detail="Name must not be empty")
    return {"message": f"Hello, {name}!", "name": name}


@app.get("/items", tags=["items"])
async def list_items() -> dict:
    """แสดงรายการ items ทั้งหมด"""
    return {"items": list(items_db.values()), "total": len(items_db)}


@app.get("/items/{item_id}", tags=["items"])
async def get_item(item_id: int) -> dict:
    """ดึงข้อมูล item ตาม ID — ตัวอย่าง 404 error handling"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return items_db[item_id]


@app.post("/items", tags=["items"], status_code=201)
async def create_item(item: ItemCreate) -> dict:
    """สร้าง item ใหม่ — ตัวอย่าง POST + request body"""
    global next_id
    new_item = {"id": next_id, **item.model_dump()}
    items_db[next_id] = new_item
    next_id += 1
    return new_item
