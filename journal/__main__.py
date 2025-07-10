import sys
from cli import app, add, list, count, exit, search, query_tag
from db import interactive_menu


# # 🏁 Main entry point for the application
# if __name__ == "__main__":
#     # If no arguments are provided, run the interactive menu
#     if len(sys.argv) == 1:
#         interactive_menu()

#     else:
#         app()
#         # If arguments are provided, run the app normally
#         # This allows the app to be used in both interactive and non-interactive modes


# 🏁 Main entry point for the application
if len(sys.argv) == 1:
    interactive_menu()
else:
    app()
    # If arguments are provided, run the app normally
    # This allows the app to be used in both interactive and non-interactive modes
