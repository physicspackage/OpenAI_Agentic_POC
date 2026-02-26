from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, Field


class AppointmentStatus(str, Enum):
    scheduled = "scheduled"
    confirmed = "confirmed"
    cancelled = "cancelled"


class Patient(BaseModel):
    id: str
    full_name: str
    dob: date
    phone: str
    email: str


class Appointment(BaseModel):
    id: str
    patient_id: str
    start_time: datetime
    provider: str
    procedure: str
    status: AppointmentStatus = AppointmentStatus.scheduled


class FollowUpTask(BaseModel):
    id: str
    patient_id: str
    description: str
    due_date: date
    completed: bool = False


class Notification(BaseModel):
    id: str
    patient_id: str
    channel: str = Field(pattern="^(sms|email)$")
    message: str
    sent_at: datetime


class AppointmentConfirmRequest(BaseModel):
    confirmed: bool = False


class FollowUpTaskCreate(BaseModel):
    patient_id: str
    description: str
    due_date: date
    confirmed: bool = False


class NotificationCreate(BaseModel):
    patient_id: str
    channel: str
    message: str
    confirmed: bool = False
