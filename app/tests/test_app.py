from fastapi.testclient import TestClient
import pytest
import uuid

from ..main import app
from .. import schemas

client = TestClient(app)


@pytest.fixture(scope="module")
def test_user():
    unique_email = f"test-{uuid.uuid4()}@example.com"
    return schemas.UserCreate(username="testuser", email=unique_email, password="test_password")


@pytest.fixture(scope="module")
def test_todo():
    unique_title = f"testtodo-{uuid.uuid4()}"
    return schemas.ToDoCreate(title=unique_title, description="Test ToDo Description", completed=False)


def test_create_user(test_user: schemas.UserCreate):
    unique_username = f"testuser-{uuid.uuid4()}"
    test_user.username = unique_username

    response = client.post("/users", json=test_user.dict())
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert "id" in data


def test_create_todo(test_user: schemas.UserCreate, test_todo: schemas.ToDoCreate):
    unique_username = f"testuser-{uuid.uuid4()}"
    test_user.username = unique_username
    user_response = client.post("/users", json=test_user.dict())
    assert user_response.status_code == 200
    user_data = user_response.json()
    user_id = user_data["id"]

    todo_response = client.post(f"/todos?user_id={user_id}", json=test_todo.dict())
    assert todo_response.status_code == 200
    todo_data = todo_response.json()
    assert todo_data["title"] == test_todo.title
    assert "id" in todo_data
    assert "completed" in todo_data
    assert not todo_data["completed"]


def test_get_todo(test_user: schemas.UserCreate, test_todo: schemas.ToDo):
    unique_username = f"testuser-{uuid.uuid4()}"
    test_user.username = unique_username
    user_response = client.post("/users", json=test_user.dict())
    user_id = user_response.json()["id"]

    todo_response = client.post(f"/todos?user_id={user_id}", json=test_todo.dict())
    todo_id = todo_response.json()["id"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_todo.title
    assert data["id"] == todo_id
    assert "completed" in data
    assert not data["completed"]


def test_get_todos(test_user: schemas.UserCreate, test_todo: schemas.ToDoCreate):
    unique_username = f"testuser-{uuid.uuid4()}"
    test_user.username = unique_username
    user_response = client.post("/users", json=test_user.dict())
    user_id = user_response.json()["id"]

    todo_response = client.post(f"/todos?user_id={user_id}", json=test_todo.dict())

    response = client.get("/todos")
    assert response.status_code == 200
    todos_data = response.json()
    assert len(todos_data) > 0


def test_update_todo(test_user: schemas.UserCreate, test_todo: schemas.ToDoCreate):
    unique_username = f"testuser-{uuid.uuid4()}"
    test_user.username = unique_username
    user_response = client.post("/users", json=test_user.dict())
    user_id = user_response.json()["id"]

    todo_response = client.post(f"/todos?user_id={user_id}", json=test_todo.dict())
    todo_id = todo_response.json()["id"]

    updated_todo = schemas.ToDoUpdate(title="Updated Title", completed=True)
    response = client.put(f"/todos/{todo_id}", json=updated_todo.dict())
    assert response.status_code == 200
    todo_data = response.json()
    assert todo_data["title"] == "Updated Title"
    assert todo_data["completed"]


def test_soft_delete_todo(test_user: schemas.UserCreate, test_todo: schemas.ToDoCreate):
    unique_username = f"testuser-{uuid.uuid4()}"
    test_user.username = unique_username
    user_response = client.post("/users", json=test_user.dict())
    user_id = user_response.json()["id"]

    todo_response = client.post(f"/todos?user_id={user_id}", json=test_todo.dict())
    todo_id = todo_response.json()["id"]

    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Todo deleted"}

    # Check if the todo is really deleted (soft delete)
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404