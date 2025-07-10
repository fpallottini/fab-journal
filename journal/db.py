import sys
from models import JournalEntry
import json
import typer
from pathlib import Path
from datetime import datetime
from uuid import uuid4
from dataclasses import dataclass, asdict, field


# 📁 File where journal entries are stored
DB_FILE = Path("journal.json")
DB_FILE.touch(exist_ok=True)


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


# Extracted function
def add_entry(title: str, content: str, tags_list: list) -> None:
    entries = load_entries()
    new_entry = JournalEntry(title=title, content=content, tags_list=tags_list)
    entries.append(new_entry)
    save_entries(entries)


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


# Interactive menu for the Journal application
def interactive_menu():
    from cli import add, list, count, exit, search, query_tag

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
