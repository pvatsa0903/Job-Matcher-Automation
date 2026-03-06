from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from job_matcher.collectors.base import is_posted_within_days, is_verified_us_location, parse_datetime
from job_matcher.models import JobPosting

STRIPE_CAREERS_URL = "https://stripe.com/jobs/search"


def parse_stripe_jobs(payload: dict[str, Any], *, now: datetime | None = None) -> list[JobPosting]:
    jobs = payload.get("data", {}).get("openings", [])
    current = now or datetime.now(timezone.utc)
    accepted: list[JobPosting] = []

    for job in jobs:
        location_info = job.get("location", {}) or {}
        location = str(location_info.get("display") or location_info.get("name") or "").strip()
        posted_at = parse_datetime(job.get("publishedAt") or job.get("postedAt"))
        if not is_verified_us_location(
            location=location,
            country_code=location_info.get("countryCode") or job.get("countryCode"),
            country_name=location_info.get("country") or job.get("country"),
        ):
            continue
        if not is_posted_within_days(posted_at, now=current):
            continue

        external_id = str(job.get("id", "")).strip()
        title = str(job.get("title", "")).strip()
        url = str(job.get("url", "")).strip() or STRIPE_CAREERS_URL
        if not external_id or not title:
            continue
        accepted.append(
            JobPosting(
                source="stripe",
                external_id=external_id,
                title=title,
                url=url,
                location=location,
                posted_at=posted_at,
                raw=job,
            )
        )
    return accepted
