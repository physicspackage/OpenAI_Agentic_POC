from __future__ import annotations

import asyncio

from rich.console import Console
from rich.panel import Panel

from .agent import run_agent


def main() -> None:
    console = Console()
    console.print(Panel("Dental Office Assistant CLI\nType 'exit' to quit.", title="POC"))

    while True:
        user_input = console.input("[bold cyan]You:[/bold cyan] ").strip()
        if user_input.lower() in {"exit", "quit"}:
            console.print("Goodbye.")
            break

        output = asyncio.run(run_agent(user_input))
        console.print(f"[bold green]Assistant:[/bold green] {output}")


if __name__ == "__main__":
    main()
