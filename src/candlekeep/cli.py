"""CandleKeep CLI - Main entry point."""

import typer
from rich.console import Console

from .commands.init import init_command

app = typer.Typer(
    name="candlekeep",
    help="A personal library that brings the wisdom of books to your AI agents",
    add_completion=False,
)

console = Console()


@app.command()
def init():
    """Initialize CandleKeep configuration and database."""
    init_command()


@app.callback()
def main():
    """CandleKeep - Your personal library for AI agents."""
    pass


if __name__ == "__main__":
    app()
