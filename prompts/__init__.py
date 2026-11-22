"""Versioned prompt templates. One file per version (vN.txt), never overwritten.

Placeholders: {labels} (comma-separated labels, EMOTIONS order unless given) and {text}.
A line `<<<USER>>>` splits a template into a system part (above) and a user part (below);
templates without it are user-only.
v1 (2026-11-19): original prompt from ollama_calls_test.py.
v2 (2026-11-21): asks for lowercase, so the answer's first token is less split across casings.
v3 (2026-11-21): v2 wording as a system message (instruction + labels); user message is only the text.
v4 (2026-11-22): v3 without "in lowercase" (capitalised answers, system message); post-hoc 2x2 check.
"""
from pathlib import Path

from data.schema import EMOTIONS

PROMPTS_DIR = Path(__file__).parent
USER_SEP = "<<<USER>>>"


def load_template(version: str) -> str:
    """Raw template text of a prompt version, e.g. "v1"."""
    return (PROMPTS_DIR / f"{version}.txt").read_text(encoding="utf-8")


def build_prompt(text: str, version: str) -> str:
    """Fill a prompt version with the fixed label list and the input text."""
    return load_template(version).format(labels=", ".join(EMOTIONS), text=text)


def build_messages(text: str, version: str, labels: list[str] | None = None) -> list[dict]:
    """Chat messages for a prompt version: [system, user] if the template has a
    USER_SEP line, else [user]. `labels` sets the label order (default EMOTIONS)."""
    fill = {"labels": ", ".join(labels or EMOTIONS)}
    template = load_template(version)
    if USER_SEP not in template:
        return [{"role": "user", "content": template.format(**fill, text=text)}]
    system, user = (part.strip("\n") for part in template.split(USER_SEP, 1))
    return [{"role": "system", "content": system.format(**fill, text=text)},
            {"role": "user", "content": user.format(**fill, text=text)}]
