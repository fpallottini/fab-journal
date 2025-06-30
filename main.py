import sys
import json
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
import typer
from uuid import uuid4


# 📁 File where journal entries are stored
DB_FILE = Path("journal.json")
DB_FILE.touch(exist_ok=True)


# 📝 Dataclass representing a journal entry
@dataclass
class JournalEntry:
    title: str
    content: str
    date: str = field(default_factory=lambda: datetime.now().isoformat())
    tags_list: list[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid4()))


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
                    tags_list=entry.get("tags_list", []),
                    id=entry.get("id", str(uuid4())),
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
def add_entry(title: str, content: str, tags_list: list) -> None:
    entries = load_entries()
    new_entry = JournalEntry(title=title, content=content, tags_list=tags_list)
    entries.append(new_entry)
    save_entries(entries)


# ➕ Add a new entry
@app.command()
def add(
    title: str = typer.Option(..., prompt="📝 Title"),
    content: str = typer.Option(..., prompt="📓 Content"),
    tags: str = typer.Option(
        "", prompt="🏷️ Tags (comma-separated)", help="Optional tags for the entry    "
    ),
):
    """➕ Add a new journal entry."""
    tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []
    add_entry(title, content, tags_list)
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
            print(
                f"🏷️ Tags: {', '.join(entry.tags_list) if entry.tags_list else 'None'}"
            )
            print(f"ID: {entry.id}")
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


# Helper function to find entries matching the query
def find_entries(entries, query):
    """Helper function to find entries matching the query."""
    q = query.lower()
    return [
        entry
        for entry in entries
        if q in entry.title.lower()
        or q in entry.content.lower()
        or q.lower() in (tag.lower() for tag in entry.tags_list)
    ]


# Helper function to find entries matching the query for tags
def find_tags(entries, query):
    """Helper function to find entries matching the query."""
    q = query.lower()
    return [
        entry
        for entry in entries
        if q.lower() in (tag.lower() for tag in entry.tags_list)
    ]


def display_results(results):
    """Helper function to display search results."""
    if not results:
        typer.echo("📭 No entries found matching your query.")
    else:
        typer.echo("📘 Your Results:")
        n = 0
        # Iterate through results and print them
        for i, entry in enumerate(results, start=1):
            n = i
            print(f"\n{n} 📅 {entry.date}")
            print(f"📓 {entry.title}")
            print(entry.content)
            print(
                f"🏷️ Tags: {', '.join(entry.tags_list) if entry.tags_list else 'None'}"
            )
            print(f"ID: {entry.id}")
            print("-" * 30)


@app.command()
def search(query: str = typer.Option(..., prompt="🔍 Enter search query")):
    """🔍 Search for entries by query."""
    entries = load_entries()
    results = find_entries(entries, query)
    display_results(results)


@app.command()
def query_tag(tag: str = typer.Option(..., prompt="🏷️ Enter tag to filter by")):
    """🔍 Filter entries by tag."""
    entries = load_entries()
    results = find_tags(entries, tag)
    display_results(results)


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
        "\n6. 🔍 Search entries"
        "\n7. 🔍 Filter entries by tag"
    )

    def add_entry_interactive():
        title = typer.prompt("📝 Title")
        content = typer.prompt("📓 Content")
        tags = typer.prompt("🏷️ Tags (comma-separated, optional)", default="")
        add(title=title, content=content, tags=tags)

    def query_tag_interactive():
        tag = typer.prompt("🏷️ Enter tag to filter by...")
        query_tag(tag=tag)

    def search_interactive():
        # always prompt for a string, so Typer’s OptionInfo never leaks through
        query = typer.prompt("🔍 Enter search query")
        # call your decorated function with an actual str
        search(query=query)

    options = {
        1: add_entry_interactive,
        2: list,
        3: count,
        4: exit,
        5: show_help,
        6: search_interactive,
        7: query_tag_interactive,
    }

    try:
        choice = typer.prompt("Enter your choice (1-7)", type=int)
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
