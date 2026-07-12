"""GH Archive downloads.

The upstream source is a multi-terabyte event firehose. This connector does
not republish raw event records; it publishes derived aggregate counts for a
recent rolling window, plus a small reference table of documented event types.
"""

from __future__ import annotations

import gzip
import io
import json
from collections import Counter
from datetime import date, datetime, timedelta, timezone

import httpx
import pyarrow as pa

from subsets_utils import NodeSpec, get, save_raw_parquet

BASE_URL = "https://data.gharchive.org"
ROLLING_DAYS = 7

DAILY_SCHEMA = pa.schema(
    [
        ("date", pa.date32()),
        ("event_type", pa.string()),
        ("event_count", pa.int64()),
    ]
)

EVENT_TYPES_SCHEMA = pa.schema(
    [
        ("event_type", pa.string()),
        ("description", pa.string()),
        ("docs_url", pa.string()),
    ]
)

DOCS_URL = "https://docs.github.com/en/rest/using-the-rest-api/github-event-types"

EVENT_TYPES = [
    ("CommitCommentEvent", "A commit comment is created."),
    ("CreateEvent", "A Git branch, tag, or repository is created."),
    ("DeleteEvent", "A Git branch or tag is deleted."),
    ("DiscussionEvent", "A discussion is created in a repository."),
    ("ForkEvent", "A user forks a repository."),
    ("GollumEvent", "A wiki page is created or updated."),
    ("IssueCommentEvent", "Activity related to an issue or pull request comment."),
    ("IssuesEvent", "Activity related to an issue."),
    ("MemberEvent", "Activity related to repository collaborators."),
    ("PublicEvent", "A private repository is made public."),
    ("PullRequestEvent", "Activity related to pull requests."),
    ("PullRequestReviewCommentEvent", "Activity related to pull request review comments."),
    ("PullRequestReviewEvent", "Activity related to pull request reviews."),
    ("PushEvent", "One or more commits are pushed to a repository branch or tag."),
    ("ReleaseEvent", "Activity related to a release."),
    ("WatchEvent", "A user stars a repository."),
]


def fetch_event_types(node_id: str) -> None:
    rows = [
        {"event_type": event_type, "description": description, "docs_url": DOCS_URL}
        for event_type, description in EVENT_TYPES
    ]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=EVENT_TYPES_SCHEMA), node_id)


def _hour_url(day: date, hour: int) -> str:
    return f"{BASE_URL}/{day.isoformat()}-{hour}.json.gz"


def _count_hour(url: str) -> Counter[str]:
    response = get(url, timeout=(10.0, 180.0))
    response.raise_for_status()

    counts: Counter[str] = Counter()
    bad_lines = 0
    with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as gz:
        for line_number, line in enumerate(gz, start=1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                bad_lines += 1
                continue
            event_type = event.get("type")
            if event_type:
                counts[str(event_type)] += 1

    if bad_lines:
        print(f"  skipped {bad_lines} malformed JSON lines in {url}")
    return counts


def _count_day(day: date) -> Counter[str]:
    counts: Counter[str] = Counter()
    for hour in range(24):
        url = _hour_url(day, hour)
        try:
            counts.update(_count_hour(url))
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                print(f"  {day.isoformat()} hour {hour}: missing upstream archive")
                continue
            raise
    return counts


def fetch_events_daily(node_id: str) -> None:
    today_utc = datetime.now(tz=timezone.utc).date()
    first_day = today_utc - timedelta(days=ROLLING_DAYS)
    last_day = today_utc - timedelta(days=1)
    rows = []

    current = first_day
    while current <= last_day:
        counts = _count_day(current)
        for event_type, event_count in sorted(counts.items()):
            rows.append(
                {
                    "date": current,
                    "event_type": event_type,
                    "event_count": event_count,
                }
            )
        print(
            f"  {current.isoformat()}: {sum(counts.values()):,} events "
            f"across {len(counts)} event types"
        )
        current += timedelta(days=1)

    if not rows:
        raise RuntimeError("no GH Archive event rows were aggregated")

    table = pa.Table.from_pylist(rows, schema=DAILY_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="gh-archive-event-types",
        fn=fetch_event_types,
        kind="download",
    ),
    NodeSpec(
        id="gh-archive-github-events-daily",
        fn=fetch_events_daily,
        kind="download",
    ),
]
