import sys
from .cli import app
from .db import interactive_menu


# 🏁 Main entry point for the application
if len(sys.argv) == 1:
    interactive_menu()
    sys.exit(0)  # Exit after the interactive menu
else:
    app()
    # If arguments are provided, run the app normally
    # This allows the app to be used in both interactive and non-interactive modes
