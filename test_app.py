import pytest
from app import app, students


@pytest.fixture
def client():
    students.clear()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
    students.clear()


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Student Management System" in response.data


def test_add_student(client):
    response = client.post("/add", data={"roll": "101", "name": "Aarav", "course": "CSE"})
    assert response.status_code == 302
    assert len(students) == 1
    assert students[0]["name"] == "Aarav"


def test_duplicate_roll_number(client):
    data = {"roll": "101", "name": "Aarav", "course": "CSE"}
    client.post("/add", data=data)
    response = client.post("/add", data={"roll": "101", "name": "Riya", "course": "IT"})
    assert response.status_code == 400
    assert len(students) == 1


def test_delete_student(client):
    client.post("/add", data={"roll": "101", "name": "Aarav", "course": "CSE"})
    response = client.post("/delete/101")
    assert response.status_code == 302
    assert len(students) == 0
