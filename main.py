# 📖 Simple Journal Application
# This is a simple command line journal application that allows users to add and list journal entries.
# It uses a JSON file to store the entries and provides a command line interface using `typer`.
# # The application allows users to add entries with a title and content, and list all entries with their
# respective dates.
# 📄 Import necessary libraries
import sys
import json
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path

# import typer for command line interface
import typer

# 📁 File where journal entries are stored
DB_FILE = Path("journal.json")
DB_FILE.touch(exist_ok=True)


# 📝 Dataclass representing a journal entry
@dataclass
class JournalEntry:
    title: str
    content: str
    date: str = field(default_factory=lambda: datetime.now().isoformat())


# 📥 Load entries from the file
def load_entries():
    if DB_FILE.stat().st_size == 0:
        return []
    with open(DB_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
        return [
            JournalEntry(
                title=entry["title"],
                content=entry["content"],
                date=entry.get("date", datetime.now().isoformat()),
            )
            for entry in data
        ]


# 💾 Save entries to the file
def save_entries(entries):
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump([asdict(entry) for entry in entries], file, indent=2)


# type for the command line interface
app = typer.Typer()


# ➕ Add a new entry
@app.command()
def add(
    title: str = typer.Option(..., prompt="Title", help="Title of the journal entry"),
    content: str = typer.Option(
        ..., prompt="Content", help="Content of the journal entry"
    ),
):
    """➕ Add a new journal entry."""
    typer.echo(f"Added entry: {title} - {content} successfully.")
    entries = load_entries()
    new_entry = JournalEntry(title=title, content=content)
    entries.append(new_entry)
    save_entries(entries)


# 📘 List journal entries
@app.command()
def list():
    """📘 List all journal entries."""
    entries = load_entries()
    if not entries:
        typer.echo("📭 No entries found.")
    else:
        typer.echo("📘 Your Journal:")
        n = 0
        # Iterate through entries and print them
        for entry in entries:
            n = n + 1
            print(f"\n{n} 📅 {entry.date}")
            print(f"📓 {entry.title}")
            print(entry.content)
            print("-" * 30)


# 📊 Count total entries
@app.command()
def count():
    """📊 Count total journal entries."""
    entries = load_entries()
    count = len(entries)
    typer.echo(f"\n 📊 Total entries 👁  in the Journal🟰 {count}")


# Exit the application
@app.command()
def exit():
    """🙌🏼 Exit the Journal application."""
    typer.echo("🙌🏼 Thank you for using the Journal! Goodbye!")
    typer.Exit(code=0)


# prompt user for CLI commands
def interactive_menu():
    typer.echo(
        "Welcome to your Journal! 📖"
        "\nChoose an option:"
        "\n1. ➕ Add a new entry: add"
        "\n2. 📘 List all entries: list"
        "\n3. 📊 Count total entries: count"
        "\n4. 🙌🏼 Exit"
        "\n5. 🛟 Help"
    )
    choice = typer.prompt("Enter your choice (1-4)", type=int)
    if choice == 1:
        add()
    elif choice == 2:
        list()
    elif choice == 3:
        count()
    elif choice == 4:
        exit()
    elif choice == 5:
        typer.echo(
            "🛟 Help: Use the commands 'add', 'list', 'count', or 'exit' to interact with your journal."
        )


# 🏁 Main entry point for the application
if __name__ == "__main__":
    # If no arguments are provided, run the interactive menu
    if len(sys.argv) == 1:
        interactive_menu()
    else:
        app()
        # If arguments are provided, run the app normally
        # This allows the app to be used in both interactive and non-interactive modes
