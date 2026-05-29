import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_home_returns_200(client):
    assert client.get("/").status_code == 200


def test_home_shows_seeded_assignments(client):
    data = client.get("/").data
    assert b"Math Homework" in data
    assert b"Essay Draft" in data


def test_add_get_returns_200(client):
    assert client.get("/add").status_code == 200


def test_add_valid_post_redirects(client):
    response = client.post("/add", data={
        "title": "Bio Lab Report",
        "class_name": "Biology",
        "due_date": "2026-07-01",
    })
    assert response.status_code == 302


def test_add_valid_post_appears_on_home(client):
    client.post("/add", data={
        "title": "Physics Problem Set",
        "class_name": "Physics",
        "due_date": "2026-07-10",
    })
    data = client.get("/").data
    assert b"Physics Problem Set" in data


def test_add_blank_title_returns_error(client):
    response = client.post("/add", data={
        "title": "",
        "class_name": "Biology",
        "due_date": "2026-07-01",
    })
    assert response.status_code == 200
    assert b"Title is required" in response.data


def test_add_blank_class_returns_error(client):
    response = client.post("/add", data={
        "title": "Essay",
        "class_name": "",
        "due_date": "2026-07-01",
    })
    assert response.status_code == 200
    assert b"Class name is required" in response.data


def test_add_blank_title_preserves_class_name(client):
    response = client.post("/add", data={
        "title": "",
        "class_name": "AP Chemistry",
        "due_date": "2026-07-01",
    })
    assert b"AP Chemistry" in response.data
