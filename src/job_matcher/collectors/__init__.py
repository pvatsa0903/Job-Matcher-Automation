from dataclasses import dataclass
from typing import Any, Callable

from job_matcher.collectors.airbnb import AIRBNB_CAREERS_URL, parse_airbnb_jobs
from job_matcher.collectors.discord import DISCORD_CAREERS_URL, parse_discord_jobs
from job_matcher.collectors.doordash import DOORDASH_CAREERS_URL, parse_doordash_jobs
from job_matcher.collectors.google import GOOGLE_CAREERS_URL, parse_google_jobs
from job_matcher.collectors.instacart import INSTACART_CAREERS_URL, parse_instacart_jobs
from job_matcher.collectors.linkedin import LINKEDIN_CAREERS_URL, parse_linkedin_jobs
from job_matcher.collectors.meta import META_CAREERS_URL, parse_meta_jobs
from job_matcher.collectors.microsoft import MS_CAREERS_URL, parse_microsoft_jobs
from job_matcher.collectors.notion import NOTION_CAREERS_URL, parse_notion_jobs
from job_matcher.collectors.pinterest import PINTEREST_CAREERS_URL, parse_pinterest_jobs
from job_matcher.collectors.reddit import REDDIT_CAREERS_URL, parse_reddit_jobs
from job_matcher.collectors.snap import SNAP_CAREERS_URL, parse_snap_jobs
from job_matcher.collectors.spotify import SPOTIFY_CAREERS_URL, parse_spotify_jobs
from job_matcher.collectors.stripe import STRIPE_CAREERS_URL, parse_stripe_jobs
from job_matcher.models import JobPosting


@dataclass(frozen=True)
class Collector:
    company: str
    official_source_url: str
    parser: Callable[[dict[str, Any]], list[JobPosting]]

    def parse(self, payload: dict[str, Any]) -> list[JobPosting]:
        return self.parser(payload)


COLLECTORS: dict[str, Collector] = {
    "airbnb": Collector("airbnb", AIRBNB_CAREERS_URL, parse_airbnb_jobs),
    "meta": Collector("meta", META_CAREERS_URL, parse_meta_jobs),
    "microsoft": Collector("microsoft", MS_CAREERS_URL, parse_microsoft_jobs),
    "reddit": Collector("reddit", REDDIT_CAREERS_URL, parse_reddit_jobs),
    "linkedin": Collector("linkedin", LINKEDIN_CAREERS_URL, parse_linkedin_jobs),
    "stripe": Collector("stripe", STRIPE_CAREERS_URL, parse_stripe_jobs),
    "spotify": Collector("spotify", SPOTIFY_CAREERS_URL, parse_spotify_jobs),
    "doordash": Collector("doordash", DOORDASH_CAREERS_URL, parse_doordash_jobs),
    "instacart": Collector("instacart", INSTACART_CAREERS_URL, parse_instacart_jobs),
    "pinterest": Collector("pinterest", PINTEREST_CAREERS_URL, parse_pinterest_jobs),
    "notion": Collector("notion", NOTION_CAREERS_URL, parse_notion_jobs),
    "snap": Collector("snap", SNAP_CAREERS_URL, parse_snap_jobs),
    "discord": Collector("discord", DISCORD_CAREERS_URL, parse_discord_jobs),
    "google": Collector("google", GOOGLE_CAREERS_URL, parse_google_jobs),
}
