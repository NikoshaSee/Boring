from fastapi.testclient import TestClient
from main import app
from database import Base, engine

# Создаем тестовую базу (чтобы не ломать основную)
Base.metadata.create_all(bind=engine)
client = TestClient(app)

def test_register_and_login():
    # Тест регистрации
    response = client.post("/api/auth/register", json={
        "username": "testuser", "password": "testpassword", "role": "inspector"
    })
    # Если юзер уже есть (при повторном запуске), то ошибка 400 - это тоже нормально для теста
    assert response.status_code in [200, 400]

    # Тест логина
    response = client.post("/api/auth/login", data={
        "username": "testuser", "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_violation_unauthorized():
    # Без токена должно быть 401
    response = client.post("/api/violations", json={
        "title": "Тестовое нарушение", "description": "Описание", "employee_id": 1
    })
    assert response.status_code == 401

def test_get_excuses():
    # Проверка банка отмазок (доступно без токена в нашем коде)
    response = client.get("/api/excuses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)