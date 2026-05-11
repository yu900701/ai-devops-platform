import argparse
from pathlib import Path
from datetime import datetime

from rich.console import Console
from tools.ci_log_analyzer import CILogAnalyzer, load_log_file, AnalysisResult


console = Console()


def render_markdown_report(result: AnalysisResult, source_log: str) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def bullet(items: list[str]) -> str:
        return "\n".join([f"- {item}" for item in items])

    next_commands = "\n".join(result.next_commands)
    truncated_log = source_log[-4000:]

    return f"""# CI Failure Analysis Report

Generated at: {now}

## Error Category

{result.category}

## Summary

{result.summary}

## Possible Causes

{bullet(result.possible_causes)}

## Suggested Fixes

{bullet(result.suggested_fixes)}

## Related Files

{bullet(result.related_files)}

## Suggested Next Commands

```bash
{next_commands}
{truncated_log}
"""

def print_result(result: AnalysisResult) -> None:
    console.rule("[bold red]CI Failure Analysis Result")
    console.print(f"[bold]Category:[/bold] {result.category}")
    console.print(f"[bold]Summary:[/bold] {result.summary}")

    console.print("\n[bold]Possible Causes:[/bold]")
    for item in result.possible_causes:
        console.print(f"- {item}")

    console.print("\n[bold]Suggested Fixes:[/bold]")
    for item in result.suggested_fixes:
        console.print(f"- {item}")

    console.print("\n[bold]Related Files:[/bold]")
    for item in result.related_files:
        console.print(f"- {item}")

    console.print("\n[bold]Suggested Next Commands:[/bold]")
    for item in result.next_commands:
        console.print(f"- {item}")

def analyze_ci(log_file: str, output_file: str) -> None:
    log_text = load_log_file(log_file)
    analyzer = CILogAnalyzer()
    result = analyzer.analyze(log_text)

    print_result(result)

    report = render_markdown_report(result, log_text)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    console.print(f"\n[green]Report generated:[/green] {output_file}")

def main() -> None:
    parser = argparse.ArgumentParser(
    description="AI DevOps Agent CLI"
    )
    subparsers = parser.add_subparsers(dest="command")

    analyze_ci_parser = subparsers.add_parser(
        "analyze-ci",
        help="Analyze CI failure log",
    )

    analyze_ci_parser.add_argument(
        "--log-file",
        required=True,
        help="Path to CI log file",
    )

    analyze_ci_parser.add_argument(
        "--output",
        default="ai-agent/outputs/ci-failure-report.md",
        help="Path to output markdown report",
    )

    args = parser.parse_args()

    if args.command == "analyze-ci":
        analyze_ci(args.log_file, args.output)
    else:
        parser.print_help()
if __name__ == "__main__":
    main()