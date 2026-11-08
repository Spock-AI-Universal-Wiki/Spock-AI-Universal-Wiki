"""Spock AI Helper — suite entry point.

Launches:
  1. Docs server (background) from pre-built site/ — port from docs_port / SPOCK_DOCS_PORT
  2. Browser to the docs URL
  3. Shared Chat AI Helper GUI (chat_ai_helper.py) over AIHelperDocuments/

Prerequisites:
  - Chat LLM reachable (configured provider / llama-server)
  - Pre-built site/ directory (build with: mkdocs build)
"""

from __future__ import annotations

import sys


def main() -> int:
    from spock_shell.paths import ensure_root_on_path

    ensure_root_on_path()

    from WarpCore.theme import THEMES
    from spock_shell.ai_helper import open_ai_helper
    from spock_shell.config import load_config

    try:
        config = load_config()
    except Exception as exc:
        print(f"Warning: could not load ship_computer settings ({exc}); using defaults.")
        config = {"ask_ai_provider": "llama-server"}

    # Docs server + browser are started inside open_ai_helper (shared with
    # Bringup Menu / suite shell AI Helper button).
    from PyQt6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication(sys.argv)
    theme = THEMES.get("dark") or next(iter(THEMES.values()))
    win = open_ai_helper(parent=None, theme=theme, config=config)  # type: ignore[arg-type]
    if win is None:
        print("Failed to open Chat AI Helper.")
        return 1
    setattr(win, "_force_close", True)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
