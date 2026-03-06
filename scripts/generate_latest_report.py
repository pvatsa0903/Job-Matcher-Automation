from __future__ import annotations

from pathlib import Path

from job_matcher.collectors import COLLECTORS
from job_matcher.scoring import SIGNAL_WEIGHTS


def build_report() -> str:
    lines: list[str] = [
        "# Latest Job Matcher Report",
        "",
        f"- Collector count: {len(COLLECTORS)}",
        f"- Priority scoring signals: {len(SIGNAL_WEIGHTS)}",
        "",
        "## Enabled Collectors",
        "",
    ]
    for company in sorted(COLLECTORS):
        collector = COLLECTORS[company]
        lines.append(f"- `{collector.company}`: {collector.official_source_url}")

    lines.extend(
        [
            "",
            "## Scoring Weights",
            "",
        ]
    )
    for signal, weight in sorted(SIGNAL_WEIGHTS.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- `{signal}`: {weight}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    report_path = Path("reports/latest.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(build_report(), encoding="utf-8")


if __name__ == "__main__":
    main()
