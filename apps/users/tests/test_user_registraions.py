# from apps.users.models import Users as UsersModel
from factories import UserFactory

from apps.users import crud
from main import app


def test_register_user__success(test_app, monkeypatch):
    test_request_payload = {
        "username": "bingoman",
        "first_name": "Jesse",
        "last_name": "Egbosionu",
        "email": "jesseinit@gmail.com",
        "password": "bigmanthing",
    }

    response = test_app.post(
        app.url_path_for("register_user"),
        json=test_request_payload,
    )

    assert response.status_code == 201
    response_data = response.json()

    assert response_data["msg"] == "Signup Successful"
    assert response_data["data"]


def test_register_user__exisiting_user(test_app, monkeypatch):
    test_request_payload = {
        "username": "bingoman",
        "first_name": "Jesse",
        "last_name": "Egbosionu",
        "email": "jesseinit@gmail.com",
        "password": "bigmanthing",
    }

    monkeypatch.setattr(
        crud, "create_user", lambda x: UserFactory(**test_request_payload)
    )
    monkeypatch.setattr(
        crud, "get_existing_user", lambda **kwargs: UserFactory(**test_request_payload)
    )

    response = test_app.post(
        app.url_path_for("register_user"),
        json=test_request_payload,
    )

    assert response.status_code == 409
    response_data = response.json()
    assert response_data["msg"] == "Username or Email has been taken"
    assert response_data["data"] == None
