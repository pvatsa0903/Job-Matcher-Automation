from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from job_matcher.collectors.base import is_posted_within_days, is_verified_us_location, parse_datetime
from job_matcher.models import JobPosting

MS_CAREERS_URL = "https://careers.microsoft.com/v2/global/en/search"


def parse_microsoft_jobs(payload: dict[str, Any], *, now: datetime | None = None) -> list[JobPosting]:
    jobs = payload.get("operationResult", {}).get("result", {}).get("jobs", [])
    current = now or datetime.now(timezone.utc)
    accepted: list[JobPosting] = []

    for job in jobs:
        location = str(job.get("primaryLocation", "")).strip()
        posted_at = parse_datetime(job.get("postingDate"))
        if not is_verified_us_location(
            location=location,
            country_code=job.get("countryCode"),
            country_name=job.get("country"),
        ):
            continue
        if not is_posted_within_days(posted_at, now=current):
            continue

        external_id = str(job.get("jobId", "")).strip()
        title = str(job.get("title", "")).strip()
        url = str(job.get("detailsUrl", "")).strip() or MS_CAREERS_URL
        if not external_id or not title:
            continue
        accepted.append(
            JobPosting(
                source="microsoft",
                external_id=external_id,
                title=title,
                url=url,
                location=location,
                posted_at=posted_at,
                raw=job,
            )
        )
    return accepted
