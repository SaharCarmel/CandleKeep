"""CandleKeep CLI - Main entry point."""

import typer
from rich.console import Console

from .commands.init import init_command
from .commands.add import add_pdf, add_md
from .commands.query import list_books, get_toc, get_pages

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


# Register add commands
app.command(name="add-pdf")(add_pdf)
app.command(name="add-md")(add_md)

# Register query commands
app.command(name="list")(list_books)
app.command(name="toc")(get_toc)
app.command(name="pages")(get_pages)


@app.callback()
def main():
    """CandleKeep - Your personal library for AI agents."""
    pass


if __name__ == "__main__":
    app()
