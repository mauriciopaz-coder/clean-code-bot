"""LLM analyzer module — connects to OpenAI or Groq to refactor code."""

import os
import re

from openai import OpenAI

from .prompts import build_refactor_prompt

# Provider-specific configuration
PROVIDER_CONFIG = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "env_key": "OPENAI_API_KEY",
        "model": "gpt-4o-mini",
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "env_key": "GROQ_API_KEY",
        "model": "llama-3.3-70b-versatile",
    },
}

# Map file extensions to language names
EXTENSION_TO_LANGUAGE = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".jsx": "javascript",
    ".tsx": "typescript",
    ".java": "java",
    ".cs": "csharp",
    ".cpp": "cpp",
    ".c": "c",
    ".h": "c",
    ".go": "go",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
    ".kt": "kotlin",
    ".rs": "rust",
    ".scala": "scala",
    ".r": "r",
    ".m": "objective-c",
}


def detect_language(filepath: str) -> str:
    """Detect programming language from file extension."""
    from pathlib import Path
    ext = Path(filepath).suffix.lower()
    return EXTENSION_TO_LANGUAGE.get(ext, "unknown")


def get_client(provider: str) -> tuple[OpenAI, str]:
    """Create an OpenAI-compatible client for the chosen provider.

    Returns (client, model_name).
    """
    if provider not in PROVIDER_CONFIG:
        raise ValueError(f"Unknown provider '{provider}'. Use 'openai' or 'groq'.")

    config = PROVIDER_CONFIG[provider]
    api_key = os.getenv(config["env_key"])

    if not api_key:
        raise ValueError(
            f"API key not found. Set {config['env_key']} in your .env file."
        )

    client = OpenAI(base_url=config["base_url"], api_key=api_key)
    return client, config["model"]


def parse_response(raw: str) -> dict:
    """Parse the structured LLM response into sections."""
    sections = {"analysis": "", "refactored_code": "", "changes_summary": "", "raw": raw}

    analysis_match = re.search(
        r"=== ANALYSIS ===(.*?)(?==== REFACTORED CODE ===)", raw, re.DOTALL
    )
    if analysis_match:
        sections["analysis"] = analysis_match.group(1).strip()

    code_match = re.search(
        r"=== REFACTORED CODE ===\s*```\w*\n(.*?)```", raw, re.DOTALL
    )
    if code_match:
        sections["refactored_code"] = code_match.group(1).strip()

    summary_match = re.search(r"=== CHANGES SUMMARY ===(.*)", raw, re.DOTALL)
    if summary_match:
        sections["changes_summary"] = summary_match.group(1).strip()

    return sections


def analyze_code(code: str, filepath: str, provider: str) -> dict:
    """Send code to the LLM for analysis and refactoring.

    Returns a dict with keys: analysis, refactored_code, changes_summary, raw.
    """
    language = detect_language(filepath)
    messages = build_refactor_prompt(code, language)

    client, model = get_client(provider)

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
        max_tokens=4096,
    )

    raw_content = response.choices[0].message.content
    return parse_response(raw_content)
