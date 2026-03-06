from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any


US_TOKENS = ("united states", "usa")


def parse_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, (int, float)):
        if value > 10_000_000_000:
            value = value / 1000
        return datetime.fromtimestamp(value, tz=timezone.utc)
    if not isinstance(value, str):
        return None

    candidate = value.strip()
    if not candidate:
        return None
    if candidate.endswith("Z"):
        candidate = candidate[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(candidate)
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except ValueError:
        pass

    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(candidate, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def is_verified_us_location(
    *,
    location: str | None,
    country_code: str | None = None,
    country_name: str | None = None,
) -> bool:
    cc = (country_code or "").strip().lower()
    cn = (country_name or "").strip().lower()
    loc = (location or "").strip().lower()

    if cc == "us":
        return True
    if cn == "united states":
        return True
    if any(token in loc for token in US_TOKENS):
        return True
    if loc.endswith(", us"):
        return True
    return False


def is_posted_within_days(
    posted_at: datetime | None,
    *,
    days: int = 7,
    now: datetime | None = None,
) -> bool:
    if posted_at is None:
        return False
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    posted = posted_at if posted_at.tzinfo else posted_at.replace(tzinfo=timezone.utc)
    age = current - posted
    return timedelta(0) <= age <= timedelta(days=days)


def extract_meta_value(meta_list: list[dict[str, Any]], key: str) -> str | None:
    lower = key.strip().lower()
    for item in meta_list:
        name = str(item.get("name", "")).strip().lower()
        if name == lower:
            value = item.get("value")
            return str(value).strip() if value else None
    return None
