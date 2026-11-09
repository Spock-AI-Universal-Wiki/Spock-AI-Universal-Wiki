"""Wiki Scan extension presets for the pre-launch filter dialog."""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

# Program / source files (languages + shell/build + structured config).
# Intentionally excludes docs: .md .html .rst .txt .adoc .pdf
PROGRAM_EXTENSIONS: Tuple[str, ...] = (
    # languages
    ".py",
    ".js",
    ".jsx",
    ".mjs",
    ".ts",
    ".tsx",
    ".vue",
    ".svelte",
    ".rs",
    ".go",
    ".java",
    ".kt",
    ".kts",
    ".swift",
    ".scala",
    ".dart",
    ".c",
    ".h",
    ".cpp",
    ".hpp",
    ".cc",
    ".cs",
    ".rb",
    ".php",
    ".lua",
    ".r",
    ".jl",
    ".ex",
    ".exs",
    ".hs",
    ".zig",
    # shell / build
    ".sh",
    ".bash",
    ".ps1",
    ".psm1",
    ".bat",
    ".cmd",
    ".gradle",
    ".cmake",
    ".tf",
    ".css",
    ".scss",
    # structured config / data used by code
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".ini",
    ".cfg",
    ".xml",
    ".proto",
    ".sql",
)

PRESET_ALL = "all"
PRESET_PROGRAM = "program"
PRESET_PROGRAM_MD = "program_md"
PRESET_PROGRAM_MD_HTML = "program_md_html"

PRESET_LABELS: Dict[str, str] = {
    PRESET_ALL: "Scan all (configured extensions)",
    PRESET_PROGRAM: "Scan program files (.py, .js, .ts, .rs, …)",
    PRESET_PROGRAM_MD: "Scan program files + .md (markdown)",
    PRESET_PROGRAM_MD_HTML: "Scan program + .md + .html (wiki site docs)",
}

PRESET_HINTS: Dict[str, str] = {
    PRESET_ALL: "Uses scan_config / Spock Console allowed_extensions (docs + code).",
    PRESET_PROGRAM: "Source, shell/build, and structured config — no markdown/HTML docs.",
    PRESET_PROGRAM_MD: "Program set plus Markdown (.md).",
    PRESET_PROGRAM_MD_HTML: "Program set plus Markdown and HTML (MkDocs / site docs).",
}


def extensions_for_preset(preset: str) -> List[str]:
    """Return sorted extension list, or empty for preset 'all' (env sentinel)."""
    key = (preset or PRESET_ALL).strip().lower()
    if key in ("", PRESET_ALL, "*", "default"):
        return []
    exts = list(PROGRAM_EXTENSIONS)
    if key == PRESET_PROGRAM_MD:
        exts.append(".md")
    elif key == PRESET_PROGRAM_MD_HTML:
        exts.extend([".md", ".html"])
    elif key != PRESET_PROGRAM:
        # Unknown → treat as all
        return []
    # de-dupe preserve order
    seen = set()
    out: List[str] = []
    for e in exts:
        el = e.lower() if e.startswith(".") else f".{e.lower()}"
        if el not in seen:
            seen.add(el)
            out.append(el)
    return out


def env_value_for_preset(preset: str) -> str:
    """Value for WIKI_AGENT_EXTENSIONS."""
    exts = extensions_for_preset(preset)
    if not exts:
        return "all"
    return ",".join(exts)


def preset_choices() -> Sequence[Tuple[str, str, str]]:
    """(id, label, hint) in display order."""
    order = (
        PRESET_ALL,
        PRESET_PROGRAM,
        PRESET_PROGRAM_MD,
        PRESET_PROGRAM_MD_HTML,
    )
    return tuple((k, PRESET_LABELS[k], PRESET_HINTS[k]) for k in order)
