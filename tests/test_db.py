import pytest
from pathlib import Path
from journal.db import JournalDatabase


@pytest.fixture(scope="function")
def db():
    db = JournalDatabase(Path("test_journal.json"))
    yield db
    # Cleanup after each test
    db.save_entries([])  # Reset the database to an empty state


def test_empty_journal(db):
    entries = db.load_entries()
    assert entries == []  # Assuming entries is an empty list initially


def test_save_entries(db):
    db.add_entry("Test Title", "Test Content", ["test", "entry"])
    entries = db.load_entries()
    assert len(entries) == 1
    entry = entries[0]
    assert entry.title == "Test Title"
    assert entry.content == "Test Content"
    assert entry.tags_list == ["test", "entry"]
