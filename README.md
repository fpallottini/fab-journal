# fab-journal
PDC Foundation – Dev Journal App - Pybites training

📖 Simple Journal Application
This is a simple command line journal application that allows users to add and list journal entries.
It uses a JSON file to store the entries and provides a command line interface using `typer`.
The application allows users to add entries with a title and content, and list all entries with their respective dates.

**PDC Foundation – Dev Journal App (Pybites training)**

A tiny but handy **journal** you can use from the terminal. It supports two ways of working:

* **CLI mode** – run discrete commands (`add`, `list`, `search`, …)
* **Interactive mode** – a guided menu you can drive with the keyboard

Entries are stored in a simple **JSON** file so they’re easy to back up, sync, or inspect.

---

## Features

* Add entries with title, content, and optional tags
* List all entries, newest first
* Count total entries
* Full-text search by query
* Filter entries by tag
* Bash/Zsh/Fish autocompletion (via Typer)
* Interactive menu for quick workflows

---

## Installation & running (uv only)

> Requires **Python 3.10+** and **[uv](https://docs.astral.sh/uv/)**.

```bash
# From the project root
uv sync                  # create/refresh the environment from pyproject.toml
uv run journal --help    # verify the CLI is available
```

On first run a `journal.json` file is created in your working directory to persist entries.

---

## Usage

### CLI mode

```bash
# Show help
uv run journal --help
```

**Available commands**

* `add` – Add a new journal entry (you’ll be prompted for fields)
* `list` – List all journal entries
* `count` – Show total number of entries
* `search` – Search entries by a free-text query
* `query-tag` – Filter entries by a specific tag
* `interactive` – Launch the interactive menu

**Examples**

```bash
# Add an entry (prompts for title/content; optionally tags)
uv run journal add

# List entries
uv run journal list

# Count how many entries you have
uv run journal count

# Search by keyword(s)
uv run journal search "pytest fixture"

# Filter by tag
uv run journal query-tag work
```

**Shell completion**

```bash
# Install completion for your current shell
uv run journal --install-completion

# Or show the script to copy/configure manually
uv run journal --show-completion
```

### Interactive mode

Prefer a guided flow? Start the menu UI:

```bash
uv run journal interactive
```

You’ll see options like:

```
1) Add a new entry
2) List all entries
3) Count total entries
4) Exit
5) Help
6) Search entries
7) Filter entries by tag
```

Use the number keys to navigate.

---

## Data model

Entries are stored as JSON objects similar to:

```json
{
  "id": "2025-03-18T10:42:15.812Z",
  "date": "2025-03-18",
  "title": "Investigated Typer callbacks",
  "content": "Notes about building a small CLI and interactive menu…",
  "tags": ["python", "cli", "notes"]
}
```

---

## Development

```bash
git clone <this-repo>
cd fab-journal
uv sync
uv run journal interactive
```

---

## Roadmap 

**M1**

* Make nicer journal outputs using the **Rich** library
* Look at test coverage (**pytest-cov**)
* *(Optional)* Use a **Makefile**
* *(Optional)* End-to-end testing of the CLI

**M2**

* Add a **PDF export** feature to the journal
* **Share your project**
* *(Optional)* Add a **NiceGUI** frontend to the Developer Journal
* *(Optional)* **Publish** the package to **PyPI**

---

## License

MIT – do whatever you like, just keep the attribution.

---

## Credits

Built for **PDC Foundation – Dev Journal App** as part of **Pybites training**.
