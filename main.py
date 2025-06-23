import sys
import json
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
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
def load_entries() -> list[JournalEntry]:
    if DB_FILE.stat().st_size == 0:
        return []
    try:
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
    except (json.JSONDecodeError, KeyError) as e:
        # If JSON is corrupted or invalid, start with empty list
        typer.echo(f"⚠️ Warning: Journal file is corrupted. Starting fresh. Error: {e}")
        # Reset the file to empty array
        with open(DB_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)
        return []


# 💾 Save entries to the file
def save_entries(entries):
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump([asdict(entry) for entry in entries], file, indent=2)


# type for the command line interface
app = typer.Typer()


# Extracted function
def add_entry(title: str, content: str) -> None:
    entries = load_entries()
    new_entry = JournalEntry(title=title, content=content)
    entries.append(new_entry)
    save_entries(entries)
    typer.echo(f"✅ Added entry: '{title}' successfully.")


# ➕ Add a new entry
@app.command()
def add(
    title: str = typer.Option(..., prompt="📝 Title"),
    content: str = typer.Option(..., prompt="📓 Content"),
):
    """➕ Add a new journal entry."""
    # If title or content are not provided, prompt for them
    if title is None:
        title = typer.prompt("Title")
    if content is None:
        content = typer.prompt("Content")
    add_entry(title, content)
    typer.echo(f"✅ Added entry: '{title}' successfully.")


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
        for i, entry in enumerate(entries, start=1):
            n = i
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


# Help function (not decorated as command, just internal)
def show_help():
    typer.echo(
        "🛟 Help: Use the commands 'add', 'list', 'count', or 'exit' to interact with your journal."
    )


# Interactive menu for the Journal application
def interactive_menu():
    typer.echo(
        "Welcome to your Journal! 📖"
        "\nChoose an option:"
        "\n1. ➕ Add a new entry"
        "\n2. 📘 List all entries"
        "\n3. 📊 Count total entries"
        "\n4. 🙌🏼 Exit"
        "\n5. 🛟 Help"
    )

    options = {
        1: lambda: add(title=None, content=None),
        2: list,
        3: count,
        4: exit,
        5: show_help,
    }

    try:
        choice = typer.prompt("Enter your choice (1-5)", type=int)
        action = options.get(choice)
        if action:
            action()
        else:
            typer.echo("❌ Invalid choice. Please enter a number from 1 to 5.")
            interactive_menu()
    except typer.Abort:
        typer.echo("\n👋 Exiting...")
    except Exception as e:
        typer.echo(f"⚠️ Error: {e}")


# 🏁 Main entry point for the application
if __name__ == "__main__":
    # If no arguments are provided, run the interactive menu
    if len(sys.argv) == 1:
        interactive_menu()

    else:
        app()
        # If arguments are provided, run the app normally
        # This allows the app to be used in both interactive and non-interactive modes
