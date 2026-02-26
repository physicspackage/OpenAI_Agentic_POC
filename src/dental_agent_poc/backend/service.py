from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any
from uuid import uuid4

from .models import (
    Appointment,
    AppointmentStatus,
    FollowUpTask,
    Notification,
    Patient,
)


class DentalService:
    def __init__(self) -> None:
        self.patients: dict[str, Patient] = {
            "p001": Patient(
                id="p001",
                full_name="Alicia Gomez",
                dob=date(1990, 7, 14),
                phone="+1-202-555-0100",
                email="alicia@example.com",
            ),
            "p002": Patient(
                id="p002",
                full_name="Marcus Lee",
                dob=date(1985, 3, 2),
                phone="+1-202-555-0199",
                email="marcus@example.com",
            ),
        }
        now = datetime.now().replace(minute=0, second=0, microsecond=0)
        self.appointments: dict[str, Appointment] = {
            "a001": Appointment(
                id="a001",
                patient_id="p001",
                start_time=now + timedelta(days=1),
                provider="Dr. Patel",
                procedure="Cleaning",
            ),
            "a002": Appointment(
                id="a002",
                patient_id="p002",
                start_time=now + timedelta(days=2),
                provider="Dr. Rivera",
                procedure="Filling",
            ),
        }
        self.tasks: dict[str, FollowUpTask] = {}
        self.notifications: dict[str, Notification] = {}

    def mask_patient(self, patient: Patient) -> dict[str, Any]:
        return {
            "id": patient.id,
            "full_name": patient.full_name,
            "dob": patient.dob.strftime("****-%m-%d"),
            "phone": patient.phone,
            "email": patient.email,
        }

    def lookup_patients(self, query: str) -> list[dict[str, Any]]:
        query = query.lower().strip()
        matches = [
            self.mask_patient(p)
            for p in self.patients.values()
            if query in p.id.lower() or query in p.full_name.lower()
        ]
        return matches

    def list_appointments(self, patient_id: str | None = None) -> list[Appointment]:
        items = list(self.appointments.values())
        if patient_id:
            items = [a for a in items if a.patient_id == patient_id]
        return sorted(items, key=lambda x: x.start_time)

    def confirm_appointment(self, appointment_id: str, confirmed: bool) -> dict[str, Any]:
        appt = self.appointments[appointment_id]
        if not confirmed:
            return {
                "confirmation_required": True,
                "preview": f"Confirm appointment {appointment_id} for patient {appt.patient_id}?",
            }
        appt.status = AppointmentStatus.confirmed
        return {"success": True, "appointment": appt.model_dump(mode="json")}

    def create_follow_up_task(
        self, patient_id: str, description: str, due_date: date, confirmed: bool
    ) -> dict[str, Any]:
        if not confirmed:
            return {
                "confirmation_required": True,
                "preview": f"Create follow-up task for {patient_id}: {description} due {due_date}",
            }
        task = FollowUpTask(
            id=f"t_{uuid4().hex[:8]}",
            patient_id=patient_id,
            description=description,
            due_date=due_date,
        )
        self.tasks[task.id] = task
        return {"success": True, "task": task.model_dump(mode="json")}

    def send_notification(
        self, patient_id: str, channel: str, message: str, confirmed: bool
    ) -> dict[str, Any]:
        if not confirmed:
            return {
                "confirmation_required": True,
                "preview": f"Send {channel} notification to {patient_id}: {message}",
            }
        notification = Notification(
            id=f"n_{uuid4().hex[:8]}",
            patient_id=patient_id,
            channel=channel,
            message=message,
            sent_at=datetime.now(),
        )
        self.notifications[notification.id] = notification
        return {
            "success": True,
            "notification": notification.model_dump(mode="json"),
        }


service = DentalService()
