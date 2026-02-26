# Dental Office Agent POC (OpenAI Agents SDK + Responses API)

Runnable proof-of-concept for a **Dental Office Assistant** agent that can:
- Look up patients
- List appointments
- Confirm appointments
- Create follow-up tasks
- Send mock notifications

The project uses:
- **OpenAI Agents SDK (Python)** for orchestration
- **Responses API** via the Agents SDK runtime
- **FastAPI** for a mock backend
- **CLI** chat interface
- Docker + docker-compose for local startup

## Architecture

- `src/dental_agent_poc/backend/api.py`: Mock backend API endpoints
- `src/dental_agent_poc/tools.py`: Tool functions that call backend endpoints
- `src/dental_agent_poc/agent.py`: Agent instructions, model, and tool wiring
- `src/dental_agent_poc/cli.py`: Interactive terminal UI

## Quickstart (local)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
```

Set `OPENAI_API_KEY` in `.env`.

### Run backend

```bash
uvicorn dental_agent_poc.backend.api:app --host 0.0.0.0 --port 8000
```

### Run CLI agent

```bash
python -m dental_agent_poc.main
```

## Docker Compose

```bash
docker compose up --build
```

This starts:
- `backend` on `localhost:8000`
- `agent-cli` container (interactive via logs/attach)

## Safety behavior in this POC

- State-changing tools (`confirm_appointment`, `create_follow_up_task`, `send_notification`) require `confirmed=true`.
- If `confirmed=false`, backend returns `confirmation_required` with a preview.
- DOB is masked in patient lookup results (`****-MM-DD`).
- Agent instruction enforces tool-only data operations and explicit confirmations.

## Tests

```bash
pytest
```

## Demo prompts

See [`docs/demo.md`](docs/demo.md).
