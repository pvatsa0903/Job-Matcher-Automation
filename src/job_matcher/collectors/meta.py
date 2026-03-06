from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from job_matcher.collectors.base import is_posted_within_days, is_verified_us_location, parse_datetime
from job_matcher.models import JobPosting

META_CAREERS_URL = "https://www.metacareers.com/jobs"


def parse_meta_jobs(payload: dict[str, Any], *, now: datetime | None = None) -> list[JobPosting]:
    jobs = payload.get("data", {}).get("jobSearch", {}).get("edges", [])
    current = now or datetime.now(timezone.utc)
    accepted: list[JobPosting] = []

    for edge in jobs:
        node = edge.get("node", {})
        location = node.get("location", {})
        posted_at = parse_datetime(node.get("postedDate"))
        location_text = location.get("name") or ""
        country_code = location.get("countryCode")
        country_name = location.get("country")
        if not is_verified_us_location(
            location=location_text,
            country_code=country_code,
            country_name=country_name,
        ):
            continue
        if not is_posted_within_days(posted_at, now=current):
            continue

        external_id = str(node.get("id", "")).strip()
        title = str(node.get("title", "")).strip()
        slug = str(node.get("slug", "")).strip()
        if not external_id or not title:
            continue
        url = f"{META_CAREERS_URL}/{slug}" if slug else META_CAREERS_URL
        accepted.append(
            JobPosting(
                source="meta",
                external_id=external_id,
                title=title,
                url=url,
                location=location_text,
                posted_at=posted_at,
                raw=node,
            )
        )
    return accepted
