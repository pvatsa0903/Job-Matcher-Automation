# Job Matcher Automation

A conservative job-collection and scoring scaffold focused on verified US roles posted within the last 7 days, with weighting tuned to Phalguni's strongest product signals.

## What This Project Does

- Collects and parses jobs from official careers sources.
- Keeps only jobs where both conditions are verifiable:
  - US location signal.
  - Posted within 7 days.
- Scores jobs using weighted resume-aligned signals:
  - growth
  - monetization
  - retention
  - lifecycle/CRM
  - experimentation
  - B2B/B2C SaaS
  - 30M+ scale
  - incentives
  - gamification
- Generates `reports/latest.md` via script and scheduled GitHub Action.

## Project Structure

- `src/job_matcher/collectors/`: company-specific parsers and collector registry.
- `src/job_matcher/scoring.py`: weighted signal scoring.
- `scripts/generate_latest_report.py`: deterministic latest report generator.
- `reports/latest.md`: generated report output.
- `tests/`: parser and scoring tests.

## Supported Collectors

- Airbnb
- Discord
- DoorDash
- Google
- Instacart
- LinkedIn
- Meta
- Microsoft
- Notion
- Pinterest
- Reddit
- Snap
- Spotify
- Stripe

## Local Setup

```bash
cd "/Users/phalgunivatsa/Documents/New project"
python3 -m unittest discover -s tests -q
```

If you want to run the report generator:

```bash
PYTHONPATH=src python3 scripts/generate_latest_report.py
```

## GitHub Action

Workflow file: `.github/workflows/scheduled-report.yml`

- Schedule target: Mon-Thu at 5:00 PM PT.
- Runs report generation.
- Opens/updates a PR only when `reports/latest.md` changed.
- Supports manual trigger via `workflow_dispatch`.

## Notes

- Parsers are intentionally strict. Ambiguous location or posting age is rejected.
- Report generation is deterministic to avoid noisy PRs.
