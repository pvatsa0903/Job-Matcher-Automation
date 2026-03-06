from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from job_matcher.collectors.base import is_posted_within_days, is_verified_us_location, parse_datetime
from job_matcher.models import JobPosting

LINKEDIN_CAREERS_URL = "https://www.linkedin.com/jobs"


def parse_linkedin_jobs(payload: dict[str, Any], *, now: datetime | None = None) -> list[JobPosting]:
    jobs = payload.get("data", {}).get("jobsSearch", {}).get("elements", [])
    current = now or datetime.now(timezone.utc)
    accepted: list[JobPosting] = []

    for job in jobs:
        location = str(job.get("formattedLocation", "")).strip()
        posted_at = parse_datetime(job.get("listedAt") or job.get("publishedAt"))
        country_code = job.get("locationCountryCode")
        country_name = job.get("locationCountry")
        if not is_verified_us_location(
            location=location,
            country_code=country_code,
            country_name=country_name,
        ):
            continue
        if not is_posted_within_days(posted_at, now=current):
            continue

        external_id = str(job.get("jobPostingUrn") or job.get("id") or "").strip()
        title = str(job.get("title", "")).strip()
        url = str(job.get("jobPostingUrl", "")).strip() or LINKEDIN_CAREERS_URL
        if not external_id or not title:
            continue
        accepted.append(
            JobPosting(
                source="linkedin",
                external_id=external_id,
                title=title,
                url=url,
                location=location,
                posted_at=posted_at,
                raw=job,
            )
        )
    return accepted
