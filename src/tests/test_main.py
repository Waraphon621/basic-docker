import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ── Fixtures ──────────────────────────────────────────────────────────────────
@pytest.fixture(autouse=True)
def reset_db():
    """Reset items_db ก่อนแต่ละ test เพื่อให้ test แยกกัน (isolated)"""
    import main as m
    m.items_db = {
        1: {"id": 1, "name": "Laptop",   "price": 35000, "in_stock": True},
        2: {"id": 2, "name": "Mouse",    "price": 450,   "in_stock": True},
        3: {"id": 3, "name": "Keyboard", "price": 1200,  "in_stock": False},
    }
    m.next_id = 4
    yield


# ── Home ──────────────────────────────────────────────────────────────────────
class TestHome:
    def test_root_status_200(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_root_returns_hello_world(self):
        response = client.get("/")
        assert response.json()["message"] == "Hello world"

    def test_root_status_is_true(self):
        response = client.get("/")
        assert response.json()["status"] is True


# ── Health ────────────────────────────────────────────────────────────────────
class TestHealth:
    def test_health_status_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_healthy(self):
        response = client.get("/health")
        assert response.json()["status"] == "healthy"

    def test_health_returns_version(self):
        response = client.get("/health")
        assert "version" in response.json()


# ── Hello ─────────────────────────────────────────────────────────────────────
class TestHello:
    def test_hello_with_name(self):
        response = client.get("/hello/pranpaveen")
        assert response.status_code == 200
        assert response.json()["message"] == "Hello, pranpaveen!"

    def test_hello_returns_name_field(self):
        response = client.get("/hello/student")
        assert response.json()["name"] == "student"

    def test_hello_different_names(self):
        for name in ["Alice", "Bob", "Charlie"]:
            response = client.get(f"/hello/{name}")
            assert response.status_code == 200
            assert name in response.json()["message"]


# ── Items ─────────────────────────────────────────────────────────────────────
class TestListItems:
    def test_list_items_status_200(self):
        response = client.get("/items")
        assert response.status_code == 200

    def test_list_items_returns_list(self):
        response = client.get("/items")
        assert isinstance(response.json()["items"], list)

    def test_list_items_total_count(self):
        response = client.get("/items")
        assert response.json()["total"] == 3


class TestGetItem:
    def test_get_existing_item(self):
        response = client.get("/items/1")
        assert response.status_code == 200
        assert response.json()["name"] == "Laptop"

    def test_get_item_not_found(self):
        response = client.get("/items/999")
        assert response.status_code == 404

    def test_get_item_not_found_message(self):
        response = client.get("/items/999")
        assert "not found" in response.json()["detail"].lower()

    def test_get_all_seed_items(self):
        for item_id in [1, 2, 3]:
            response = client.get(f"/items/{item_id}")
            assert response.status_code == 200


class TestCreateItem:
    def test_create_item_status_201(self):
        payload = {"name": "Monitor", "price": 8500, "in_stock": True}
        response = client.post("/items", json=payload)
        assert response.status_code == 201

    def test_create_item_returns_new_item(self):
        payload = {"name": "Monitor", "price": 8500}
        response = client.post("/items", json=payload)
        data = response.json()
        assert data["name"] == "Monitor"
        assert data["price"] == 8500
        assert data["in_stock"] is True   # default value

    def test_create_item_increments_id(self):
        payload = {"name": "Webcam", "price": 1500}
        response = client.post("/items", json=payload)
        assert response.json()["id"] == 4   # หลังจาก 3 seed items

    def test_create_item_appears_in_list(self):
        payload = {"name": "Headset", "price": 2000}
        client.post("/items", json=payload)
        response = client.get("/items")
        names = [item["name"] for item in response.json()["items"]]
        assert "Headset" in names

    def test_create_item_missing_required_field(self):
        payload = {"price": 100}   # ขาด name
        response = client.post("/items", json=payload)
        assert response.status_code == 422   # Unprocessable Entity
