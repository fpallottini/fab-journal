import typer
from .db import (
    add_entry,
    load_entries,
    show_help,
    find_entries,
    find_tags,
    display_results,
)


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


@app.command()
def interactive():
    """🛠️ Start interactive mode."""
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

    def exit_interactive():
        typer.echo("🙌🏼 Thank you for using the Journal! Goodbye!")
        raise typer.Abort()

    options = {
        1: add_entry_interactive,
        2: list,
        3: count,
        4: exit_interactive,
        5: show_help,
        6: search_interactive,
        7: query_tag_interactive,
    }
    num_options = len(options)

    while True:
        try:
            choice = typer.prompt(f"Enter your choice (1-{num_options})", type=int)
            action = options.get(choice)
            if action:
                action()
            else:
                typer.echo(f"❌ Invalid choice. Please enter a number from 1 to {num_options}.")
                continue
        except typer.Abort:
            typer.echo("\n👋 Exiting...")
            break
        except Exception as e:
            typer.echo(f"⚠️ Error: {e}")
