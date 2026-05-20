# Basic Docker — Lab Repository

FastAPI demo สำหรับสอน **Docker** และ **Docker Compose**

---

## โครงสร้าง Repository

```
basic-docker/
├── src/                        ← Source code (FastAPI + Tests)
│   ├── main.py                 ← API endpoints
│   └── tests/
│       └── test_main.py        ← pytest tests (21 tests)
│
├── lab1-docker/                ← Lab 1: Docker Build & Run
├── lab2-compose/               ← Lab 2: Docker Compose
├── lab2b-examples/             ← Lab 2b: Compose examples
│   ├── network-example/        ← Multi-service networking
│   ├── volume-bind/            ← Bind mount example
│   └── volume-shared/          ← Shared named volume
│
├── docs/                       ← Slides & lab guide (PDF)
├── Dockerfile                  ← Build image
├── docker-compose.yml          ← Multi-container setup (app + redis)
└── requirements.txt
```

---

## Labs

| Lab | หัวข้อ |
|-----|--------|
| [Lab 1](./lab1-docker/) | Docker Build & Run |
| [Lab 2](./lab2-compose/) | Docker Compose |
| [Lab 2b](./lab2b-examples/) | Compose Examples (network/volumes) |

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Hello world |
| GET | `/health` | Health check |
| GET | `/hello/{name}` | Personalized greeting |
| GET | `/items` | List all items |
| GET | `/items/{item_id}` | Get item by ID |
| POST | `/items` | Create new item |

ดู Swagger UI ที่ http://localhost:8000/docs หลัง `docker compose up`

---

## Quick Start

```bash
# Clone
git clone https://github.com/layel2/basic-docker.git
cd basic-docker

# Build & Run (Docker)
docker build -t testapi .
docker run -p 8000:8000 testapi

# Run tests
docker run testapi pytest -v

# Docker Compose (app + redis)
docker compose up -d
```
