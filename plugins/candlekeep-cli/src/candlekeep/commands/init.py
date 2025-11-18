"""Init command - initialize CandleKeep configuration."""

import subprocess
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

console = Console()


def init_command():
    """Initialize CandleKeep configuration and database."""
    candlekeep_dir = Path.home() / ".candlekeep"
    library_dir = candlekeep_dir / "library"
    originals_dir = candlekeep_dir / "originals"
    db_path = candlekeep_dir / "candlekeep.db"

    # Check if already initialized
    if candlekeep_dir.exists() and db_path.exists():
        console.print("[yellow]⚠ CandleKeep is already initialized.[/yellow]")
        console.print(f"Database: {db_path}")
        console.print(f"Library: {library_dir}")

        if not Confirm.ask("Do you want to reinitialize?", default=False):
            console.print("[cyan]Initialization cancelled.[/cyan]")
            return

    console.print(
        Panel.fit(
            "[bold cyan]CandleKeep Initialization[/bold cyan]\n\n"
            "Setting up your local library with SQLite database.",
            border_style="cyan"
        )
    )

    # Create directories
    console.print("\n[cyan]Creating directories...[/cyan]")
    candlekeep_dir.mkdir(parents=True, exist_ok=True)
    library_dir.mkdir(parents=True, exist_ok=True)
    originals_dir.mkdir(parents=True, exist_ok=True)
    console.print(f"[green]✓[/green] Created {candlekeep_dir}")
    console.print(f"[green]✓[/green] Created {library_dir}")
    console.print(f"[green]✓[/green] Created {originals_dir}")

    # Run Alembic migrations
    console.print("\n[cyan]Initializing database...[/cyan]")
    try:
        result = subprocess.run(
            ["uv", "run", "alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            check=True
        )
        console.print("[green]✓[/green] Database schema created")
    except subprocess.CalledProcessError as e:
        console.print(f"[red]✗ Failed to create database schema[/red]")
        console.print(f"Error: {e.stderr}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Unexpected error: {e}[/red]")
        raise typer.Exit(1)

    # Success message
    console.print(
        Panel.fit(
            "[bold green]✓ CandleKeep initialized successfully![/bold green]\n\n"
            f"Database: {db_path}\n"
            f"Library: {library_dir}\n"
            f"Originals: {originals_dir}\n\n"
            "You can now add books with: [cyan]candlekeep add-pdf <file>[/cyan]",
            border_style="green"
        )
    )
