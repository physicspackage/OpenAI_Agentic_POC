from __future__ import annotations

from datetime import date
from typing import Any

import httpx
from agents import function_tool

from .config import settings


def _client() -> httpx.Client:
    return httpx.Client(base_url=settings.backend_base_url, timeout=20.0)


@function_tool
def lookup_patients(query: str) -> dict[str, Any]:
    """Look up patients by ID or partial name."""
    with _client() as client:
        response = client.get("/patients", params={"query": query})
        response.raise_for_status()
        return response.json()


@function_tool
def list_appointments(patient_id: str | None = None) -> dict[str, Any]:
    """List appointments, optionally filtering by patient ID."""
    with _client() as client:
        response = client.get("/appointments", params={"patient_id": patient_id})
        response.raise_for_status()
        return response.json()


@function_tool
def confirm_appointment(appointment_id: str, confirmed: bool = False) -> dict[str, Any]:
    """Confirm an appointment. Requires confirmed=true for state change."""
    with _client() as client:
        response = client.post(
            f"/appointments/{appointment_id}/confirm", json={"confirmed": confirmed}
        )
        response.raise_for_status()
        return response.json()


@function_tool
def create_follow_up_task(
    patient_id: str, description: str, due_date: str, confirmed: bool = False
) -> dict[str, Any]:
    """Create a follow-up task for a patient. Requires confirmed=true for state change."""
    # Input validation for predictable behavior
    date.fromisoformat(due_date)
    with _client() as client:
        response = client.post(
            "/tasks",
            json={
                "patient_id": patient_id,
                "description": description,
                "due_date": due_date,
                "confirmed": confirmed,
            },
        )
        response.raise_for_status()
        return response.json()


@function_tool
def send_notification(
    patient_id: str, channel: str, message: str, confirmed: bool = False
) -> dict[str, Any]:
    """Send a mock patient notification via sms or email. Requires confirmed=true for state change."""
    with _client() as client:
        response = client.post(
            "/notifications",
            json={
                "patient_id": patient_id,
                "channel": channel,
                "message": message,
                "confirmed": confirmed,
            },
        )
        response.raise_for_status()
        return response.json()
