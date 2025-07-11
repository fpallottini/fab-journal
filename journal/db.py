from .models import JournalEntry
import json
import typer
from pathlib import Path
from datetime import datetime
from uuid import uuid4
from dataclasses import asdict


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
