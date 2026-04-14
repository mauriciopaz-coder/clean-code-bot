"""Input sanitization module to prevent prompt injection attacks."""

import re

# Patterns that indicate prompt injection attempts
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|above|prior)\s+(instructions|prompts|rules)",
    r"disregard\s+(all\s+)?(previous|above|prior)",
    r"you\s+are\s+now\s+a",
    r"act\s+as\s+(a\s+)?",
    r"new\s+instructions?\s*:",
    r"system\s*:\s*",
    r"<\|im_start\|>",
    r"<\|im_end\|>",
    r"\[INST\]",
    r"\[/INST\]",
    r"<<SYS>>",
    r"<</SYS>>",
    r"ASSISTANT\s*:",
    r"HUMAN\s*:",
    r"USER\s*:",
]

MAX_FILE_SIZE_BYTES = 100_000  # 100 KB limit
ALLOWED_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".java", ".cs", ".cpp", ".c", ".h",
    ".go", ".rb", ".php", ".swift", ".kt",
    ".rs", ".scala", ".r", ".m",
}


def check_file_extension(filepath: str) -> str | None:
    """Validate that the file has an allowed code extension.

    Returns an error message if invalid, None if valid.
    """
    from pathlib import Path
    ext = Path(filepath).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_EXTENSIONS))
        return f"Unsupported file extension '{ext}'. Allowed: {allowed}"
    return None


def check_file_size(content: str) -> str | None:
    """Validate that file content doesn't exceed the size limit.

    Returns an error message if too large, None if valid.
    """
    size = len(content.encode("utf-8"))
    if size > MAX_FILE_SIZE_BYTES:
        return (
            f"File too large ({size:,} bytes). "
            f"Maximum allowed: {MAX_FILE_SIZE_BYTES:,} bytes."
        )
    return None


def check_prompt_injection(content: str) -> str | None:
    """Scan content for prompt injection patterns.

    Returns an error message if injection detected, None if clean.
    """
    for pattern in INJECTION_PATTERNS:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return (
                f"Potential prompt injection detected: '{match.group()}'. "
                f"Input rejected for security reasons."
            )
    return None


def sanitize_input(filepath: str, content: str) -> str | None:
    """Run all validation checks on the input file.

    Returns an error message if any check fails, None if all pass.
    """
    checks = [
        check_file_extension(filepath),
        check_file_size(content),
        check_prompt_injection(content),
    ]
    for error in checks:
        if error is not None:
            return error
    return None
