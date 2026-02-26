from fastapi.testclient import TestClient

from dental_agent_poc.backend.api import app


client = TestClient(app)


def test_patient_lookup_masks_dob() -> None:
    response = client.get("/patients", params={"query": "Alicia"})
    assert response.status_code == 200
    item = response.json()["items"][0]
    assert item["dob"].startswith("****-")


def test_confirm_requires_confirmation_flag() -> None:
    response = client.post("/appointments/a001/confirm", json={"confirmed": False})
    assert response.status_code == 200
    assert response.json()["confirmation_required"] is True


def test_create_task_success_when_confirmed() -> None:
    response = client.post(
        "/tasks",
        json={
            "patient_id": "p001",
            "description": "Post-cleaning callback",
            "due_date": "2026-01-12",
            "confirmed": True,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["task"]["patient_id"] == "p001"
