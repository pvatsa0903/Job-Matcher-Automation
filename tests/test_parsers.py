import unittest
from datetime import datetime, timezone

from job_matcher.collectors.airbnb import parse_airbnb_jobs
from job_matcher.collectors.discord import parse_discord_jobs
from job_matcher.collectors.doordash import parse_doordash_jobs
from job_matcher.collectors.google import parse_google_jobs
from job_matcher.collectors.instacart import parse_instacart_jobs
from job_matcher.collectors.linkedin import parse_linkedin_jobs
from job_matcher.collectors.meta import parse_meta_jobs
from job_matcher.collectors.microsoft import parse_microsoft_jobs
from job_matcher.collectors.notion import parse_notion_jobs
from job_matcher.collectors.pinterest import parse_pinterest_jobs
from job_matcher.collectors.reddit import parse_reddit_jobs
from job_matcher.collectors.snap import parse_snap_jobs
from job_matcher.collectors.spotify import parse_spotify_jobs
from job_matcher.collectors.stripe import parse_stripe_jobs

NOW = datetime(2026, 3, 5, 12, 0, tzinfo=timezone.utc)


class ParserTests(unittest.TestCase):
    def test_meta_parser_keeps_only_verified_us_recent_jobs(self) -> None:
        payload = {
            "data": {
                "jobSearch": {
                    "edges": [
                        {
                            "node": {
                                "id": "m-1",
                                "title": "Software Engineer",
                                "slug": "software-engineer",
                                "postedDate": "2026-03-03T09:00:00Z",
                                "location": {"name": "Menlo Park, CA, United States", "countryCode": "US"},
                            }
                        },
                        {
                            "node": {
                                "id": "m-2",
                                "title": "SWE",
                                "postedDate": "2026-03-03T09:00:00Z",
                                "location": {"name": "London, UK", "countryCode": "GB"},
                            }
                        },
                    ]
                }
            }
        }
        parsed = parse_meta_jobs(payload, now=NOW)
        self.assertEqual([job.external_id for job in parsed], ["m-1"])

    def test_microsoft_parser_requires_recency(self) -> None:
        payload = {
            "operationResult": {
                "result": {
                    "jobs": [
                        {
                            "jobId": "ms-1",
                            "title": "Site Reliability Engineer",
                            "postingDate": "2026-03-04",
                            "primaryLocation": "Redmond, WA, US",
                            "countryCode": "US",
                            "detailsUrl": "https://careers.microsoft.com/job/ms-1",
                        },
                        {
                            "jobId": "ms-2",
                            "title": "SRE",
                            "postingDate": "2026-02-20",
                            "primaryLocation": "Redmond, WA, US",
                            "countryCode": "US",
                        },
                    ]
                }
            }
        }
        parsed = parse_microsoft_jobs(payload, now=NOW)
        self.assertEqual([job.external_id for job in parsed], ["ms-1"])

    def test_reddit_parser_requires_verified_us_location(self) -> None:
        payload = {
            "jobs": [
                {
                    "id": 101,
                    "title": "Backend Engineer",
                    "absolute_url": "https://reddit.com/jobs/101",
                    "updated_at": "2026-03-02T00:00:00Z",
                    "location": {"name": "Remote - United States"},
                    "metadata": [{"name": "Country Code", "value": "US"}],
                },
                {
                    "id": 102,
                    "title": "Backend Engineer",
                    "absolute_url": "https://reddit.com/jobs/102",
                    "updated_at": "2026-03-02T00:00:00Z",
                    "location": {"name": "Remote - Canada"},
                    "metadata": [{"name": "Country Code", "value": "CA"}],
                },
            ]
        }
        parsed = parse_reddit_jobs(payload, now=NOW)
        self.assertEqual([job.external_id for job in parsed], ["101"])

    def test_linkedin_parser_keeps_recent_us_jobs(self) -> None:
        payload = {
            "data": {
                "jobsSearch": {
                    "elements": [
                        {
                            "jobPostingUrn": "urn:li:jobPosting:1",
                            "title": "Product Engineer",
                            "jobPostingUrl": "https://linkedin.com/jobs/view/1",
                            "listedAt": int(datetime(2026, 3, 4, 10, 0, tzinfo=timezone.utc).timestamp() * 1000),
                            "formattedLocation": "New York, NY, United States",
                            "locationCountryCode": "US",
                        },
                        {
                            "jobPostingUrn": "urn:li:jobPosting:2",
                            "title": "Product Engineer",
                            "listedAt": int(datetime(2026, 2, 1, 10, 0, tzinfo=timezone.utc).timestamp() * 1000),
                            "formattedLocation": "New York, NY, United States",
                            "locationCountryCode": "US",
                        },
                    ]
                }
            }
        }
        parsed = parse_linkedin_jobs(payload, now=NOW)
        self.assertEqual([job.external_id for job in parsed], ["urn:li:jobPosting:1"])

    def test_spotify_parser_requires_us_signal(self) -> None:
        payload = {
            "jobs": [
                {
                    "id": 301,
                    "title": "Data Engineer",
                    "absolute_url": "https://spotify.com/jobs/301",
                    "created_at": "2026-03-01T08:00:00Z",
                    "location": {"name": "Boston, MA, US"},
                    "metadata": [],
                },
                {
                    "id": 302,
                    "title": "Data Engineer",
                    "created_at": "2026-03-01T08:00:00Z",
                    "location": {"name": "Berlin, Germany"},
                    "metadata": [{"name": "Country Code", "value": "DE"}],
                },
            ]
        }
        parsed = parse_spotify_jobs(payload, now=NOW)
        self.assertEqual([job.external_id for job in parsed], ["301"])

    def test_discord_parser_filters_out_old_jobs(self) -> None:
        payload = {
            "jobs": [
                {
                    "id": 401,
                    "title": "Developer Relations Engineer",
                    "absolute_url": "https://discord.com/jobs/401",
                    "updated_at": "2026-03-05T01:00:00Z",
                    "location": {"name": "San Francisco, CA, United States"},
                    "metadata": [{"name": "Country", "value": "United States"}],
                },
                {
                    "id": 402,
                    "title": "Developer Relations Engineer",
                    "updated_at": "2026-01-10T01:00:00Z",
                    "location": {"name": "San Francisco, CA, United States"},
                    "metadata": [{"name": "Country", "value": "United States"}],
                },
            ]
        }
        parsed = parse_discord_jobs(payload, now=NOW)
        self.assertEqual([job.external_id for job in parsed], ["401"])

    def test_google_parser_requires_verified_us_and_recent(self) -> None:
        payload = {
            "jobs": [
                {
                    "id": "g-1",
                    "title": "Software Engineer",
                    "applyUrl": "https://careers.google.com/jobs/results/g-1",
                    "publishTime": "2026-03-05T05:00:00Z",
                    "locations": [{"display": "Sunnyvale, CA, United States", "countryCode": "US"}],
                },
                {
                    "id": "g-2",
                    "title": "Software Engineer",
                    "publishTime": "2026-03-05T05:00:00Z",
                    "locations": [{"display": "Toronto, Canada", "countryCode": "CA"}],
                },
            ]
        }
        parsed = parse_google_jobs(payload, now=NOW)
        self.assertEqual([job.external_id for job in parsed], ["g-1"])

    def test_airbnb_parser_keeps_only_verified_us_recent_jobs(self) -> None:
        payload = {
            "jobs": [
                {
                    "id": 501,
                    "title": "Infra Engineer",
                    "absolute_url": "https://careers.airbnb.com/501",
                    "updated_at": "2026-03-04T02:00:00Z",
                    "location": {"name": "San Francisco, CA, US"},
                    "metadata": [],
                },
                {
                    "id": 502,
                    "title": "Infra Engineer",
                    "updated_at": "2026-03-04T02:00:00Z",
                    "location": {"name": "Paris, France"},
                    "metadata": [{"name": "Country Code", "value": "FR"}],
                },
            ]
        }
        parsed = parse_airbnb_jobs(payload, now=NOW)
        self.assertEqual([job.external_id for job in parsed], ["501"])

    def test_stripe_parser_requires_recent_us_openings(self) -> None:
        payload = {
            "data": {
                "openings": [
                    {
                        "id": "st-1",
                        "title": "Backend Engineer",
                        "url": "https://stripe.com/jobs/listing/st-1",
                        "publishedAt": "2026-03-03T10:00:00Z",
                        "location": {"display": "Seattle, WA, United States", "countryCode": "US"},
                    },
                    {
                        "id": "st-2",
                        "title": "Backend Engineer",
                        "publishedAt": "2026-02-01T10:00:00Z",
                        "location": {"display": "Seattle, WA, United States", "countryCode": "US"},
                    },
                ]
            }
        }
        parsed = parse_stripe_jobs(payload, now=NOW)
        self.assertEqual([job.external_id for job in parsed], ["st-1"])

    def test_doordash_parser_filters_non_us_jobs(self) -> None:
        payload = {
            "jobs": [
                {
                    "id": 601,
                    "title": "Machine Learning Engineer",
                    "absolute_url": "https://careers.doordash.com/601",
                    "updated_at": "2026-03-02T10:00:00Z",
                    "location": {"name": "New York, NY, United States"},
                    "metadata": [{"name": "Country Code", "value": "US"}],
                },
                {
                    "id": 602,
                    "title": "Machine Learning Engineer",
                    "updated_at": "2026-03-02T10:00:00Z",
                    "location": {"name": "Vancouver, Canada"},
                    "metadata": [{"name": "Country Code", "value": "CA"}],
                },
            ]
        }
        parsed = parse_doordash_jobs(payload, now=NOW)
        self.assertEqual([job.external_id for job in parsed], ["601"])

    def test_instacart_parser_filters_old_jobs(self) -> None:
        payload = {
            "jobs": [
                {
                    "id": 701,
                    "title": "Data Scientist",
                    "absolute_url": "https://instacart.careers/701",
                    "updated_at": "2026-03-01T10:00:00Z",
                    "location": {"name": "Remote, United States"},
                    "metadata": [{"name": "Country", "value": "United States"}],
                },
                {
                    "id": 702,
                    "title": "Data Scientist",
                    "updated_at": "2026-01-01T10:00:00Z",
                    "location": {"name": "Remote, United States"},
                    "metadata": [{"name": "Country", "value": "United States"}],
                },
            ]
        }
        parsed = parse_instacart_jobs(payload, now=NOW)
        self.assertEqual([job.external_id for job in parsed], ["701"])

    def test_pinterest_parser_requires_verified_us_location(self) -> None:
        payload = {
            "jobs": [
                {
                    "id": 801,
                    "title": "iOS Engineer",
                    "absolute_url": "https://pinterest.com/jobs/801",
                    "updated_at": "2026-03-04T10:00:00Z",
                    "location": {"name": "Chicago, IL, US"},
                    "metadata": [],
                },
                {
                    "id": 802,
                    "title": "iOS Engineer",
                    "updated_at": "2026-03-04T10:00:00Z",
                    "location": {"name": "Mexico City, Mexico"},
                    "metadata": [{"name": "Country Code", "value": "MX"}],
                },
            ]
        }
        parsed = parse_pinterest_jobs(payload, now=NOW)
        self.assertEqual([job.external_id for job in parsed], ["801"])

    def test_notion_parser_keeps_recent_us_jobs_only(self) -> None:
        payload = {
            "jobs": [
                {
                    "id": 901,
                    "title": "Security Engineer",
                    "absolute_url": "https://www.notion.so/careers/901",
                    "created_at": "2026-03-04T00:00:00Z",
                    "location": {"name": "New York, NY, United States"},
                    "metadata": [],
                },
                {
                    "id": 902,
                    "title": "Security Engineer",
                    "created_at": "2026-03-04T00:00:00Z",
                    "location": {"name": "Dublin, Ireland"},
                    "metadata": [{"name": "Country Code", "value": "IE"}],
                },
            ]
        }
        parsed = parse_notion_jobs(payload, now=NOW)
        self.assertEqual([job.external_id for job in parsed], ["901"])

    def test_snap_parser_validates_country_and_age(self) -> None:
        payload = {
            "jobPostings": [
                {
                    "jobId": "sn-1",
                    "jobTitle": "Frontend Engineer",
                    "externalPath": "/jobs/sn-1",
                    "postedOn": "2026-03-05T00:00:00Z",
                    "location": "Santa Monica, CA, United States",
                    "countryCode": "US",
                },
                {
                    "jobId": "sn-2",
                    "jobTitle": "Frontend Engineer",
                    "externalPath": "/jobs/sn-2",
                    "postedOn": "2026-03-05T00:00:00Z",
                    "location": "London, UK",
                    "countryCode": "GB",
                },
            ]
        }
        parsed = parse_snap_jobs(payload, now=NOW)
        self.assertEqual([job.external_id for job in parsed], ["sn-1"])


if __name__ == "__main__":
    unittest.main()
