"""Compatibility shim — Wiki Scan panel lives in ``spock_wiki_adapter.wiki_run``."""

from spock_wiki_adapter.wiki_run import (  # noqa: F401
    ProcessOutputReader,
    build_wiki_agent_run_panel,
    strip_ansi,
)
