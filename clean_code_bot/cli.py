"""Clean Code Bot — CLI entry point."""

import sys
from pathlib import Path

import click
from dotenv import load_dotenv

from .analyzer import analyze_code
from .sanitizer import sanitize_input


@click.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option(
    "--provider",
    type=click.Choice(["openai", "groq"], case_sensitive=False),
    default="groq",
    help="LLM provider to use (default: groq).",
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    default=None,
    help="Output file path. If omitted, prints to stdout.",
)
@click.option(
    "--full",
    is_flag=True,
    default=False,
    help="Show full output including analysis and change summary.",
)
def main(filepath: str, provider: str, output: str | None, full: bool) -> None:
    """Refactor a code file using LLM-powered analysis.

    FILEPATH is the path to the source code file to refactor.

    \b
    Examples:
        clean-code-bot dirty_code.py
        clean-code-bot app.js --provider openai
        clean-code-bot utils.py -o utils_clean.py --full
    """
    load_dotenv()

    # Read the input file
    path = Path(filepath)
    click.echo(f"Reading {path.name}...")
    content = path.read_text(encoding="utf-8")

    # Validate and sanitize input
    click.echo("Validating input...")
    error = sanitize_input(filepath, content)
    if error:
        click.secho(f"Error: {error}", fg="red", err=True)
        sys.exit(1)

    click.secho("Input validated successfully.", fg="green")

    # Send to LLM for analysis
    click.echo(f"Analyzing code with {provider}... (this may take a moment)")
    try:
        result = analyze_code(content, filepath, provider)
    except ValueError as e:
        click.secho(f"Configuration error: {e}", fg="red", err=True)
        sys.exit(1)
    except Exception as e:
        click.secho(f"API error: {e}", fg="red", err=True)
        sys.exit(1)

    if not result["refactored_code"]:
        click.secho(
            "Warning: Could not parse refactored code from response. "
            "Showing raw output.",
            fg="yellow",
            err=True,
        )
        click.echo(result["raw"])
        sys.exit(1)

    # Display or save results
    if full:
        click.secho("\n=== ANALYSIS ===", fg="cyan", bold=True)
        click.echo(result["analysis"])
        click.secho("\n=== REFACTORED CODE ===", fg="cyan", bold=True)

    if output:
        out_path = Path(output)
        out_path.write_text(result["refactored_code"] + "\n", encoding="utf-8")
        click.secho(f"\nRefactored code saved to {out_path}", fg="green")
    else:
        click.echo(result["refactored_code"])

    if full:
        click.secho("\n=== CHANGES SUMMARY ===", fg="cyan", bold=True)
        click.echo(result["changes_summary"])

    click.secho("\nDone!", fg="green", bold=True)


if __name__ == "__main__":
    main()
