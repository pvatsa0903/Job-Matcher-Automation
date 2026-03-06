from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class JobPosting:
    source: str
    external_id: str
    title: str
    url: str
    location: str
    posted_at: datetime
    raw: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "external_id": self.external_id,
            "title": self.title,
            "url": self.url,
            "location": self.location,
            "posted_at": self.posted_at.astimezone(timezone.utc).isoformat(),
            "raw": self.raw,
        }
