from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from job_matcher.collectors.base import is_posted_within_days, is_verified_us_location, parse_datetime
from job_matcher.models import JobPosting

GOOGLE_CAREERS_URL = "https://www.google.com/about/careers/applications/jobs/results"


def parse_google_jobs(payload: dict[str, Any], *, now: datetime | None = None) -> list[JobPosting]:
    jobs = payload.get("jobs", [])
    current = now or datetime.now(timezone.utc)
    accepted: list[JobPosting] = []

    for job in jobs:
        locations = job.get("locations", []) or []
        primary_loc = locations[0] if locations else {}
        location = str(primary_loc.get("display") or primary_loc.get("name") or "").strip()
        country_code = primary_loc.get("countryCode") or job.get("countryCode")
        country_name = primary_loc.get("country") or job.get("country")
        posted_at = parse_datetime(job.get("publishTime") or job.get("postedDate"))
        if not is_verified_us_location(
            location=location,
            country_code=country_code,
            country_name=country_name,
        ):
            continue
        if not is_posted_within_days(posted_at, now=current):
            continue

        external_id = str(job.get("id", "")).strip()
        title = str(job.get("title", "")).strip()
        url = str(job.get("applyUrl", "")).strip() or GOOGLE_CAREERS_URL
        if not external_id or not title:
            continue
        accepted.append(
            JobPosting(
                source="google",
                external_id=external_id,
                title=title,
                url=url,
                location=location,
                posted_at=posted_at,
                raw=job,
            )
        )
    return accepted
