from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from job_matcher.collectors.base import (
    extract_meta_value,
    is_posted_within_days,
    is_verified_us_location,
    parse_datetime,
)
from job_matcher.models import JobPosting

DISCORD_CAREERS_URL = "https://boards-api.greenhouse.io/v1/boards/discord/jobs"


def parse_discord_jobs(payload: dict[str, Any], *, now: datetime | None = None) -> list[JobPosting]:
    jobs = payload.get("jobs", [])
    current = now or datetime.now(timezone.utc)
    accepted: list[JobPosting] = []

    for job in jobs:
        metadata = job.get("metadata", []) or []
        location = str(job.get("location", {}).get("name", "")).strip()
        posted_at = parse_datetime(job.get("updated_at") or job.get("created_at"))
        if not is_verified_us_location(
            location=location,
            country_code=extract_meta_value(metadata, "country code"),
            country_name=extract_meta_value(metadata, "country"),
        ):
            continue
        if not is_posted_within_days(posted_at, now=current):
            continue

        external_id = str(job.get("id", "")).strip()
        title = str(job.get("title", "")).strip()
        url = str(job.get("absolute_url", "")).strip() or DISCORD_CAREERS_URL
        if not external_id or not title:
            continue
        accepted.append(
            JobPosting(
                source="discord",
                external_id=external_id,
                title=title,
                url=url,
                location=location,
                posted_at=posted_at,
                raw=job,
            )
        )
    return accepted
