from dental_agent_poc.agent import INSTRUCTIONS


def test_instruction_mentions_confirmation_and_tools() -> None:
    low = INSTRUCTIONS.lower()
    assert "state-changing" in low
    assert "ask for explicit confirmation" in low
    assert "do not invent" in low
