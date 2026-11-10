# Spock: A Local-First Agentic Software Engineering Workstation for Gemma and Gemini on Consumer Hardware

**Subtitle:** Best New Resource — an open workstation that makes Gemma, EmbeddingGemma, and Gemini usable for grounded GitHub and wiki comprehension on everyday hardware  
**Track:** Google Gemma 4 Developer Agent — Paper Track  
**Artifacts:** 
· [github.com/Spock-AI-Universal-Wiki/Spock-AI-Universal-Wiki](https://github.com/Spock-AI-Universal-Wiki/Spock-AI-Universal-Wiki) 
· [Docs](https://spock-ai-universal-wiki.github.io/Spock-AI-Universal-Wiki/) 
· [Screenshot gallery](https://spock-ai-universal-wiki.github.io/Spock-AI-Universal-Wiki/gallery/)

---

## Abstract

Cloud coding agents are powerful, but many developers still need agents that run **offline or on consumer GPUs**, with answers grounded in *their* repositories rather than generic web knowledge. This Paper Track submission presents **Spock** as a **Best New Resource**: an open, multi-platform agentic software-engineering workstation—not a new Gemma 4 post-training recipe.

Spock productizes the missing ops and retrieval substrate: hardware-aware model acquisition (llmfit + Hub shortlists), dual llama-server roles (embedding + chat), hybrid SQLite FTS5 + vector RAG (`ship_computer.db`), GitHub/wiki ingestion, Ask AI / Deep Dive over scoped corpora, an MCP HTTP adapter for IDE clients, and first-class **Google / Gemma / Gemini** paths (GGUF catalogs, EmbeddingGemma profiles, OpenAI-compatible and Vertex/Gemini connectors). A dedicated **Spock AI Helper** answers installation and usage questions about Spock itself from curated `AIHelperDocuments/`, so bring-up is assisted rather than tribal knowledge. Spock runs on **Windows, WSL, Linux Ubuntu, and Apple Silicon (macOS)**.

The public artifact is Apache-2.0 source, MkDocs documentation, and a captioned screenshot gallery. Judges can reproduce without Competition Data: clone, bootstrap, acquire a Gemma-family GGUF (or point at Gemini - OpenAI,or Vertex), ingest ANY github repo, ask grounded questions, and optionally connect MCP.

---

## Introduction

Today’s strongest coding agents assume internet-connected frontier models and cloud sandboxes. The Gemma 4 Developer Agent program asks a complementary question: how do we make **agentic software engineering** practical on everyday hardware? The main track ranks agents by bugs fixed. This Paper Track asks for research and resources that advance the field. Spock answers as **software**—a shippable workstation—aligned with the official Best New Resource example of tools that help explore GitHub repositories and related code structure.

Most open “local LLM” projects stop at a chat UI or a single server binary. Agentic SE fails for a different reason: **the model is often not the bottleneck—the workstation is**. Engineers need (a) models that fit detected VRAM before download, (b) an embedding service co-hosted with chat so RAG does not starve generation, (c) ingestion of moving codebases without a cloud index, (d) tools the IDE agent can call, and (e) human-scale help when installation stalls. Spock treats those as product surfaces—Acquire, Ship Status, Wiki Scan / GitHub fetch, Ask AI / Deep Dive, MCP, Provider allow-list, and **AI Helper**—instead of undocumented scripts.

Spock does not claim a custom Gemma 4 reward model, PEFT leaderboard CSV, or private Competition Data. Where Gemma 4 appears in catalogs or ID tests, we document **support and operability**. Demo hosts may run Gemma 2/3 GGUFs; the writeup says so. Honesty is part of verifiability. The claim is narrower and stronger for a resource prize: others can clone Spock and stand up a Google-forward, grounded coding assistant stack on consumer hardware across four OS families.

Spock grew out of my own questions about other people’s GitHub repositories. My first AI project was a YouTube Channel Curator: a local chat assistant that answered questions about YouTube content and helped build playlists and favorite-channel lists. I quickly saw the same need for source code—asking grounded questions about another author’s repository to supplement their documentation.
Spock is a local-hosted answer to that problem. It can ingest a GitHub repo such as llmfit or llama.cpp, support multi-turn Deep Dive over the supplied source, and compare that corpus with a target project to inform planning, design, and implementation. Google tools and resources (including Gemma, EmbeddingGemma, and Gemini connectors) were used to complete this Best New Resource submission for the Gemma 4 Developer Agent Paper Track.

## Methods and experiments

### Architecture

Spock separates reusable packages (`spock_bringup`, `spock_rag_adapter`, `spock_mcp_adapter`, …) from mission-control stations (Navigation, Engineering Deck, Science Station, Long Range Sensors / UIEG - Universal Ingestion Engine Google) over a shared kernel (**WarpCore**) and a local SQLite system of record (`ship_computer.db`).

```text
┌──────────────────────────────────────────────────────────────┐
│ Stations: Navigation · Engineering · Science · UIEG          │
│ Tools: AI Helper · Ship Status · Google Search / Gemini      │
└───────────────┬──────────────────────────────┬───────────────┘
                │                              │
     ┌──────────▼──────────┐        ┌──────────▼──────────┐
     │ llama-server roles  │        │ MCP HTTP adapter    │
     │ embed + chat ports  │        │ IDE / Cursor tools  │
     └──────────┬──────────┘        └─────────────────────┘
                │
     ┌──────────▼──────────┐
     │ ship_computer.db    │  documents · chunks · FTS5 · embeddings · logs
     │ uieg_capture.db     │  ingest (wiki scan / GitHub fetch / crawl)
     └──────────▲──────────┘
                │ 
     ┌──────────┴──────────┐
     │ Providers           │  google/… Gemma GGUF · EmbeddingGemma · Gemini
     │ allow-list or ALL   │  LM Studio · Ollama · OpenAI-compatible
     └─────────────────────┘
```

**Platforms.** The same resource targets:

| Platform            | Entry path                                                |
| ------------------- | --------------------------------------------------------- |
| Windows 10/11       | `Setup-Spock.bat` / `Spock-Menu.bat`, Phase A/B bootstrap |
| WSL                 | `spock_menu.sh` / `bootstrap.sh`                          |
| Linux Ubuntu        | `Linux-Ubuntu-Setup-README.md` (CUDA peer)                |
| Apple Silicon macOS | `Apple-Silicon-Setup-README.md` (Metal llama-server)      |

**Provider allow-list.** Maintenance can restrict Acquire / Hub / Launch lists to `google` (or any orgs). Zero rows means all providers—Google-forward demos without vendor lock-in.

### Spock AI Helper (installation and usage aid)

A Best New Resource fails if only the author can operate it. **Spock AI Helper** is a first-class tool for answering questions **about Spock itself**—bring-up, stations, ports, models, and workflows—rather than about an arbitrary user codebase (that is Ask AI / Deep Dive’s job).

**Why it exists.** Local agent stacks fail in the first hour: which server must be up, which GGUF role is embedding vs chat, how Provider filters work, where scan roots live. Static docs help, but operators ask follow-ups. AI Helper turns the curated how-to corpus into an interactive assistant.

**How it works.**

1. **Launch.** `Spock-AI-Helper.bat` (or `helper_main.py`) starts a lightweight PyQt6 chat UI and, when configured, a local docs server for the pre-built MkDocs `site/` (typically port **8000**).
2. **Prerequisites.** A chat LLM must be reachable—commonly local `llama-server` on **:8081** (`/health`, `/v1/chat/completions`) after Navigation Launch writes readiness (`spock_ready_last.json`). AI Helper unlocks once chat is healthy; it is also available from station **Tools** panes after bring-up step 4.
3. **Corpus.** Answers are grounded in curated Markdown under `AIHelperDocuments/` (Bringup Menu, Navigation Launch, Bootstrap Wizard, UIEG, system specs, and Ask-AI transcripts that capture operational Q&A). Ranking boosts helper-named docs; top snippets are assembled into a system prompt that instructs the model to use **only** that context and admit gaps.
4. **Generation.** A background worker posts an OpenAI-compatible chat completion to the local chat endpoint so the GUI stays responsive. Optionally, suite integrations can also consult hybrid search / embeddings against `ship_computer.db` when the helper is wired through the fuller onboarding path.
5. **Scope.** Designed questions include: how first launch / Phase A–B works; how Acquire picks fit models; what ports mean; how to open Ask AI vs Deep Dive; how MCP is started; how Provider=`google` changes Hub lists. It is **not** the cross-repo engineering analyst—that remains Engineering Deck Ask AI / Deep Dive over ingested trees.

**Experiment (resource usability).** After bootstrap and Launch, open AI Helper and ask: “How does Spock AI Helper work?” and “When is AI Helper unlocked?” Expect answers citing helper docs and launch prerequisites—evidence that the resource documents itself for new operators. Gallery slug `spock-chat-ai-helper-panel` shows the chat UI in Ready state.

### Bring-up and hardware-aware Acquire

**Bootstrap.** Phase A creates `.venv` and UI deps; Phase B installs fuller requirements and writes `bootstrap_full_deps.ok`. Bring-up CLI/GUI initializes `ship_computer.db` with operator profiles and uieg_capture.db (universal ingest engine google) that can ingest / wiki scan / GitHub fetch / web crawl.

**Acquire.** Hardware profiling (CPU, RAM, GPU VRAM / Metal unified memory) feeds a shortlist that merges llmfit signals, Hub rows, and catalog policy. Embedding models stay light and resident; chat GGUFs scale with VRAM. Runtime writes `-ngl` / context / thread hints into local config. With Provider=`google`, shortlists emphasize Google-provided Gemma-family chat rows and EmbeddingGemma profiles.

### Code comprehension experiments (GitHub → RAG → Ask / Deep Dive)

These are **operability experiments** for a resource paper—not competition private-leaderboard scores.

1. **Ingest.** UIEG / GitHub Fetch captures a repository (or local clone -language agnostic); filters drop `node_modules`/binaries; preview before index. 
2. **Index.** Chunks land in `ship_computer.db` with FTS5 + embeddings (EmbeddingGemma or configured profile), including Matryoshka-style dimension options where supported.
3. **Ask AI.** Path-scoped questions (“Explain WarpCore DB init”) return grounded answers with document hits.
4. **Deep Dive.** Broader investigations compare multiple roots (e.g., Spock vs an llmfit tree): retrieve labeled snippets per repo, synthesize differences, persist evidence trails in the ship computer for audit/resume.
5. **Hybrid cloud (optional).** Configure OpenAI-compatible Gemini/Vertex for chat while keeping embeddings and the corpus local—large-context synthesis without abandoning the ship computer.

### MCP as the agent I/O bus

The MCP adapter exposes Spock tools over HTTP so IDE agents (e.g., Cursor) can drive ingestion/status without reimplementing the workstation. MCP reference panel documents listen ports and tool lists; Ship Status / probes make failures visible (PIDs, endpoints, pass/fail counts) IDE agents can use eight different commands to query Spock.

### Reproduce smoke path (verifiability)

Public artifacts: GitHub source, Docs, Gallery, Apache-2.0. No Competition Data; secrets stay gitignored (`.env`, `app_config.json`, `*.db`, GGUF weights).

1. Clone on Windows, WSL, Ubuntu, or Apple Silicon; follow the matching setup README.  
2. Phase A–B bootstrap.  
3. Optional: Provider allow-list `google`.  
4. Acquire embedding + Gemma-family chat GGUFs (or configure Gemini); start servers; confirm Ship Status.  
5. Open **AI Helper**; ask an install/usage question about Spock.  
6. Ingest this repo or a sample tree; confirm embedding health.  
7. Ask AI / Deep Dive a grounded code question.  
8. Start MCP; list tools from a client.

### Gallery evidence (Google / Gemma / Gemini)

| Gallery slug                                   | Verifies                                           |
| ---------------------------------------------- | -------------------------------------------------- |
| `spock-hf-chat-models-list`                    | Google-provided HF chat models                     |
| `spock-navigation-station-gemma-quantizations` | Gemma GGUF quant table                             |
| `spock-model-selection-panel`                  | Local GGUFs including EmbeddingGemma               |
| `spock-configure-ai-*`                         | LM Studio / Ollama / OpenAI-compatible / llama.cpp |
| `spock-google-search-view`                     | In-app Google Search                               |
| `spock-navigation-station-ai-chat`             | Gemini pane                                        |
| `spock-mcp-*-panel`                            | MCP listen + tool reference                        |
| `spock-ask-ai-*`                               | Ask / Deep Dive UX                                 |
| `spock-chat-ai-helper-panel`                   | AI Helper install/usage chat                       |
| `spock-embedding-profile-rag-api-panel`        | Embedding / RAG controls                           |

GitHub Actions builds MkDocs + gallery to Pages. Absence of committed secrets is intentional negative evidence.

---

## Related work and citations

**Local llama.cpp / Ollama UIs** expose chat and sometimes model download, but rarely unify VRAM-aware acquire, dual embed/chat roles, SQLite hybrid RAG, GitHub ingest, MCP, and self-help for the suite itself.

**IDE coding assistants** (Continue-style RAG, cloud agents) excel inside the editor yet often assume SaaS indexes or API models. Spock keeps the ship computer local and optional Gemini as a connector, and exposes tools via MCP so the IDE agent can call the workstation.

**SWE-bench / contest agents** optimize patch success under harness constraints. Spock does not replace that leaderboard; it supplies the **developer-side resource** those agents (and humans) need to bring up Gemma-class stacks and comprehend repos on consumer hardware—the Paper Track’s Best New Resource niche ([Markowitz et al., 2026](https://www.kaggle.com/competitions/gemma-4-developer-agent-paper)).

**RAG systems** commonly separate vector DBs from apps. Spock’s contribution is productization: stations, probes, Provider policy, AI Helper over `AIHelperDocuments/`, and cross-platform bootstrap (Windows / WSL / Ubuntu / Apple Silicon Metal) as one Apache-2.0 artifact.

---

## Conclusion

Spock is submitted as a **Best New Resource**: open software, documentation, and screenshot evidence for local agentic software engineering with Google / Gemma / Gemini paths.

- Apache-2.0 public GitHub + live docs + gallery  
- Multi-platform: Windows, WSL, Linux Ubuntu, Apple Silicon  
- Hardware-aware Acquire and dual-model hosting  
- Hybrid RAG + Ask / Deep Dive over GitHub/wiki corpora  
- **AI Helper** for Spock installation and usage Q&A  
- MCP adapter for IDE agents  
- Reproduce path without Competition Data; no fabricated Gemma 4 RL claims  

**Not claimed:** new Gemma 4 post-training, private Vertex credentials in-tree, or main-track private-leaderboard scores. **Claimed:** a verifiable workstation resource that operationalizes grounded, Google-forward agentic SE on consumer hardware.


