from __future__ import annotations

from fastapi import FastAPI, HTTPException

from .models import (
    AppointmentConfirmRequest,
    FollowUpTaskCreate,
    NotificationCreate,
)
from .service import service

app = FastAPI(title="Mock Dental Backend API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/patients")
def lookup_patients(query: str) -> dict[str, object]:
    return {"items": service.lookup_patients(query)}


@app.get("/appointments")
def list_appointments(patient_id: str | None = None) -> dict[str, object]:
    return {"items": [a.model_dump(mode="json") for a in service.list_appointments(patient_id)]}


@app.post("/appointments/{appointment_id}/confirm")
def confirm_appointment(appointment_id: str, payload: AppointmentConfirmRequest) -> dict[str, object]:
    if appointment_id not in service.appointments:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return service.confirm_appointment(appointment_id, payload.confirmed)


@app.post("/tasks")
def create_follow_up_task(payload: FollowUpTaskCreate) -> dict[str, object]:
    if payload.patient_id not in service.patients:
        raise HTTPException(status_code=404, detail="Patient not found")
    return service.create_follow_up_task(
        payload.patient_id,
        payload.description,
        payload.due_date,
        payload.confirmed,
    )


@app.post("/notifications")
def send_notification(payload: NotificationCreate) -> dict[str, object]:
    if payload.patient_id not in service.patients:
        raise HTTPException(status_code=404, detail="Patient not found")
    return service.send_notification(
        payload.patient_id,
        payload.channel,
        payload.message,
        payload.confirmed,
    )
