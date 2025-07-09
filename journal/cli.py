import typer
from .models import JournalEntry
from .db import add_entry, load_entries, save_entries, show_help, find_entries, find_tags, display_results, interactive_menu


# type for the command line interface
app = typer.Typer()


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