import json

import pytest

from apps.notes import crud
from apps.notes.models import Notes as NotesModel


def test_create_note(test_app, monkeypatch):
    test_request_payload = {"title": "something", "description": "something else"}
    test_response_payload = {
        "id": "e6466ac4-aa66-49c8-96fd-4fc616bc502e",
        "title": "something",
        "description": "something else",
    }

    def mock_post(payload):
        mocked_note = NotesModel(**test_response_payload)
        return mocked_note

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post(
        "/notes",
        json=test_request_payload,
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_note_invalid_json(test_app):
    response = test_app.post("/notes", json={"title": "something"})
    assert response.status_code == 422


def test_read_all_notes(test_app, monkeypatch):
    test_data = [
        {
            "title": "something",
            "description": "something else",
            "id": "e6466ac4-aa66-49c8-96fd-4fc616bc502e",
        },
        {
            "title": "someone",
            "description": "someone else",
            "id": "e6466ac4-aa66-49c8-96fd-4fc616bc502e",
        },
    ]

    def mock_get_all():
        return [NotesModel(**data) for data in test_data]

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/notes")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_note(test_app, monkeypatch):
    test_data = {
        "id": "e6466ac4-aa66-49c8-96fd-4fc616bc502e",
        "title": "something",
        "description": "something else",
    }

    def mock_get(id):
        return NotesModel(**test_data)

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get(f"/notes/{test_data['id']}")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_note_incorrect_id(test_app, monkeypatch):
    def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/notes/1a267873-30c0-48cf-adfd-e3cb26c53c79")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


def test_update_note(test_app, monkeypatch):
    test_update_data = {
        "title": "someone",
        "description": "someone else",
        "id": "1a267873-30c0-48cf-adfd-e3cb26c53c79",
    }

    def mock_get(id):
        return NotesModel(**test_update_data)

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(
        f"/notes/{test_update_data['id']}", data=json.dumps(test_update_data)
    )
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"description": "bar"}, 422],
        [
            "1a267873-30c0-48cf-adfd-e3cb26c53c79",
            {"title": "foo", "description": "bar"},
            404,
        ],
    ],
)
def test_update_note_invalid(test_app, monkeypatch, id, payload, status_code):
    def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/notes/{id}", json=payload)
    assert response.status_code == status_code


def test_remove_note(test_app, monkeypatch):
    test_data = {
        "title": "something",
        "description": "something else",
        "id": "1a267873-30c0-48cf-adfd-e3cb26c53c79",
    }

    def mock_get(id):
        return NotesModel(**test_data)

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete(f"/notes/{test_data['id']}")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_note_incorrect_id(test_app, monkeypatch):
    def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/notes/1a267873-30c0-48cf-adfd-e3cb26c53c79")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"
