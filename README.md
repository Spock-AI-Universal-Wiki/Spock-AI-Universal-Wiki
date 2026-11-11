# Spock-AI-Universal-Wiki

**Spock** is a local-first agentic software-engineering workstation: hardware-aware bring-up, hybrid RAG over your codebase/wiki, MCP tools for IDE agents, and first-class connectors for **Google / Gemma / Gemini** (local GGUF + cloud) on consumer GPUs.

> Offline-capable agents need more than weights — they need ops + retrieval substrate. Spock is that open resource.

## Live docs & screenshots

| Resource | URL |
| --- | --- |
| Docs (MkDocs) | https://spock-ai-universal-wiki.github.io/Spock-AI-Universal-Wiki/ |
| Screenshot gallery | https://spock-ai-universal-wiki.github.io/Spock-AI-Universal-Wiki/gallery/ |
| Source | https://github.com/Spock-AI-Universal-Wiki/Spock-AI-Universal-Wiki |

## Why Spock (Best New Resource framing)

* **Hardware-aware acquire** — llmfit + Hub shortlists sized to VRAM; provider allow-list (e.g. Google-only) in Maintenance → Provider.
* **Hybrid RAG** — SQLite FTS5 + embeddings (`ship_computer.db`) for grounded Ask AI / Deep Dive.
* **MCP surface** — Cursor and other clients get Spock tools over HTTP.
* **Google-forward** — Gemma GGUF catalogs, EmbeddingGemma profiles, Gemini / Vertex connectors, in-app Google Search + Gemini panel.

## **Spock-AI-Universal-Wiki Feature Summary**

* **Wiki Agent**
  
  * **Description:** Crawls, indexes, and queries local or remote wiki content OR github repository. It extracts text, stores structured results in SQLite, and supports application queries such as Ask AI and Deep Dive workflows.
  * **Source Path:** `\spock-ai-universal-wiki\docs\features\wiki-agent.md`
* **Engineering Deck**
  
  * **Description:** A specialized suite of tools providing maintenance capabilities, health checks, and ship-computer diagnostics to monitor, diagnose, and repair critical systems.
  * **Source Path:** `\spock-ai-universal-wiki\docs\features\engineering-deck.md`
* **Science Station (Hybrid AI Architecture)**
  
  * **Description:** Employs a dedicated embedding model, a local vector database (optimized for approximate nearest neighbor search), and a generative LLM to separate semantic retrieval from content generation.
  * **Source Path:** `\spock-ai-universal-wiki\docs\features\science-station.md`
* **RAG API Server**
  
  * **Description:** Integrates with the `ship_computer.db` SQLite database to ensure user questions are answered using relevant context from the knowledge base, while maintaining a queryable record of requests and system actions.
  * **Source Path:** `\spock-ai-universal-wiki\docs\features\rag-api-server.md`
* **Chat AI Helper (`chat_ai_helper.py`)**
  
  * **Description:** A helper script that provides suite how-to Q&A from `AIHelperDocuments` using a chat LLM.
  * **Source Path:** `\spock-ai-universal-wiki\docs\structure\root-scripts.md`
* **SQLite Grid Browser (`db_browser.py`)**
  
  * **Description:** A utility that provides SQLite grid browsing for `ship_computer.db` along with a file preview dialog.
  * **Source Path:** `\spock-ai-universal-wiki\docs\structure\root-scripts.md`
* **Database Maintenance Utility (`db_maintenance.py`)**
  
  * **Description:** A dedicated database maintenance utility containing 34 functions to manage and maintain the `ship_computer.db` database.
  * **Source Path:** `\spock-ai-universal-wiki\docs\structure\root-scripts.md`
* **`spock_bringup` CLI**
  
  * **Description:** A command-line interface supporting environment bring-up tasks via `acquire`, `up`, `status`, and `down` commands.
  * **Source Path:** `\spock-ai-universal-wiki\docs\reference\plan-summary.md`
* **`spock_probe` Health Verification**
  
  * **Description:** A tool that performs health verification and writes a readiness contract (`spock_ready_last.json`).
  * **Source Path:** `\spock-ai-universal-wiki\docs\reference\plan-summary.md`
* **`spock_shell` PyQt6 GUI**
  
  * **Description:** A PyQt6 graphical user interface skeleton designed for managing and interacting with the application's workstations.
  * **Source Path:** `\spock-ai-universal-wiki\docs\reference\plan-summary.md`
  
  > **Spock-to-bridge**: The bridge console for a personal Starfleet knowledge base.Scan hardware, find and launch GGUF models, watch the ship’s computer ingest files,and ask the AI against `ship_computer.db` embeddings.
  
  ## What Is This?
  
  **Spock is a PyQt6 desktop application that ties together:
  
  1. **Hardware assessment** (ported from Spock-Scanner) — can this machine run local LLMs?
  2. **Model selection** (ported from Spock-Model-Selector) — find GGUF models on Hugging Face, download them, read model cards, launch `llama-server`
  3. **Ship’s computer / RAG** — SQLite knowledge base with hybrid search (vector + FTS5) and an AI chat panel
  4. **Wiki Agent** — background ingestion that watches folders, extracts text, and writes embeddings
  5. **MCP adapter** — stdio FastMCP tools for Cursor / OpenCode (`scripts/mcp_spock_server.py`)
  
  The UI uses a left navigation rail, a swappable middle pane, and a right “AI Settings” dock. The window title is **Spock Navigation Station**, with a Vulcan-salute application icon.
  
  ### The Bridge Crew (ingestion agent)
  
  | Officer | Role | Responsibilities |
  | --- | --- | --- |
  | **Computer** | Agent loop | Boot, queue management, file watching, status reporting |
  | **Scotty** | Chief Engineer | File extraction (PDF, DOCX, HTML, TXT), embeddings |
  | **Bones** | Security | Secret scanning, quarantine, forbidden pattern detection |
  | **Kirk** | Commanding Officer | Index generation, backups, cron scheduling |
  | **Spock** | Science Officer | Maintenance, orphan detection, lint reports |
  

## Quick start (Windows)

    Spock-Menu.bat

Or console menu: Spock-Menu-Console

Linux / WSL peer: chmod +x spock_menu.sh bootstrap.sh ./spock_menu.sh

Apple Silicon (macOS) peer — see [`Apple-Silicon-Setup-README.md`](Apple-Silicon-Setup-README.md): chmod +x spock_menu.sh bootstrap.sh Spock-Menu.sh ./bootstrap.sh --phase-a && ./Spock-Menu.sh

## Local docs / gallery preview

    # Main docs (needs docs deps in .venv)
    pip install -r requirements-docs.txt
    mkdocs serve -a 127.0.0.1:8000
    
    # Screenshot gallery (JPEG captions from LM Studio prescan)
    cd gallery
    python -m mkdocs serve -a 127.0.0.1:8001

Pre-scan ShareX PNGs from `assets/` (not committed; regenerated into `gallery/docs/images/`): powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\prescan-screenshots.ps1

## Google / Gemma / Gemini support

* **Acquire / HF / Launch** — filter by provider (`google`, …); empty list = all providers.
* **Configure AI** — LM Studio, Ollama, llama.cpp, OpenAI-compatible, Vertex / Gemini paths.
* **Tools panel** — Google Search and Gemini beside the station workflows.
* **Gallery** — captioned UI evidence for HF Gemma lists, provider panels, Search/Gemini, EmbeddingGemma, MCP, Ask AI.

## What stays local (never commit)

* `.env`, `app_config.json`, HF/API tokens, Vertex project IDs
* `*.db`, `models/**`, GGUF weights, `tools/**` binaries
* Raw ShareX `assets/*.png` (published shots live under `gallery/docs/images/`)

## License

Apache License 2.0 — see [LICENSE](LICENSE)
