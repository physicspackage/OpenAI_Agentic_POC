from __future__ import annotations

from agents import Agent, Runner

from .config import settings
from .tools import (
    confirm_appointment,
    create_follow_up_task,
    list_appointments,
    lookup_patients,
    send_notification,
)

INSTRUCTIONS = """
You are a Dental Office Assistant for {practice_name}.
You are responsible for dental appointment scheduling, patient lookup, appointment confirmations, task creation, and notifications.
You must use controlled tools to perform all state-changing actions.
You must summarize planned actions before executing them and ask for explicit confirmation unless user says 'confirm'.
Do not invent or hallucinate patient or appointment data.
Protect PHI and avoid exposing full DOB unless required; keep logs masked.
Respond clearly and professionally and return structured responses when appropriate.
Keep summaries brief.
""".strip()


def build_agent() -> Agent:
    return Agent(
        name="Dental Office Assistant",
        instructions=INSTRUCTIONS.format(practice_name=settings.practice_name),
        model=settings.model,
        tools=[
            lookup_patients,
            list_appointments,
            confirm_appointment,
            create_follow_up_task,
            send_notification,
        ],
    )


async def run_agent(user_input: str) -> str:
    agent = build_agent()
    result = await Runner.run(agent, user_input)
    return str(result.final_output)
