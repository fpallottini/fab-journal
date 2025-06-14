import json
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path

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
        return [JournalEntry(**entry) for entry in data]


# 💾 Save entries to the file
def save_entries(entries):
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump([asdict(entry) for entry in entries], file, indent=2)


# ➕ Add a new entry
def add_entry(title, content):
    entries = load_entries()
    new_entry = JournalEntry(title=title, content=content)
    entries.append(new_entry)
    save_entries(entries)


# 📃 List all entries
def list_entries(entries):
    for entry in entries:
        print(f"\n📅 {entry.date}")
        print(f"📓 {entry.title}")
        print(entry.content)
        print("-" * 30)


# 🚀 Main program (interactive)
if __name__ == "__main__":
    title = input("Title: ")
    content = input("Content: ")
    add_entry(title, content)
    print("✅ Entry saved.")
    print("\n📘 Your Journal:")
    list_entries(load_entries())
