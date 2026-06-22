"""Baseball Savant Statcast pitch-by-pitch firehose.

**Statcast pitch-by-pitch** (1 spec) — the granular "details" corpus from
`/statcast_search/csv`. This endpoint is hard-capped at 25,000 rows per query,
so the corpus (~700k pitches/season, ~8M rows across the era) must be windowed
by date. We walk 3-day windows from the start of the Statcast era to today and
re-pull the full corpus every run (raw is run-scoped in this harness, so each
run rebuilds its own snapshot — no cross-run watermark). The pitch CSV header is
identical across every season, so each window is stored as raw gzipped CSV bytes
verbatim (no per-row Python coercion — that does not scale to ~8M rows); DuckDB's
read_csv_auto types the ~119 columns at transform time.

This is a genuinely distinct fetch body from the leaderboard family (different
endpoint, date-windowing, gzip raw storage), so it lives in its own file. The SQL
transform is a thin parse-and-publish pass (`SELECT *`).
"""

from datetime import datetime, timezone, timedelta
import gzip

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_file

from utils import SLUG, STATCAST_ERA_START, _fetch_csv_text

# statcast_search hard-caps any query at 25,000 rows. A full MLB day is ~3,000-5,500
# pitches, so a 3-day window (~16k worst case) stays comfortably under the cap.
STATCAST_ROW_CAP = 25000
STATCAST_WINDOW_DAYS = 3


# ---------------------------------------------------------------------------
# Statcast pitch-by-pitch (date-windowed, stateless full re-pull)
# ---------------------------------------------------------------------------
# Raw is run-scoped in this harness (runs/<run_id>/raw/...) while state is durable
# across runs, so a watermark-gated firehose would let a later run skip fetching
# yet land its raw in a fresh, empty scope. The corpus is therefore re-pulled in
# full every run: walk every window from the start of the Statcast era to today
# and write one gzipped-CSV batch per window into this run's raw scope.

def fetch_statcast_pitches(node_id: str) -> None:
    cur = STATCAST_ERA_START
    end = datetime.now(timezone.utc).date()
    n_batches = 0

    while cur <= end:
        win_end = min(cur + timedelta(days=STATCAST_WINDOW_DAYS - 1), end)
        url = (
            "https://baseballsavant.mlb.com/statcast_search/csv?all=true&type=details"
            f"&player_type=pitcher&game_date_gt={cur.isoformat()}"
            f"&game_date_lt={win_end.isoformat()}"
        )
        text = _fetch_csv_text(url)
        cur = win_end + timedelta(days=1)
        if text is None:
            continue  # transient/permanent skip already logged
        if text and text[0] == "﻿":
            text = text[1:]
        # data-row count = lines minus the single header line. statcast CSV cells
        # never contain embedded newlines, so a line count is exact and avoids
        # parsing 8M rows in Python.
        n_data = max(0, len(text.splitlines()) - 1)
        if n_data >= STATCAST_ROW_CAP:
            # window hit the server's row cap -> truncated; shrink and retry.
            raise RuntimeError(
                f"{node_id}: window returned {n_data} rows "
                f"(>= cap {STATCAST_ROW_CAP}); reduce STATCAST_WINDOW_DAYS"
            )
        if n_data > 0:
            # store raw CSV bytes (gzip) verbatim; the SQL transform types it via
            # DuckDB read_csv_auto. No per-row Python coercion -> fast at 8M rows.
            save_raw_file(
                gzip.compress(text.encode("utf-8")),
                f"{node_id}-{win_end.isoformat()}",
                extension="csv.gz",
            )
            n_batches += 1

    if n_batches == 0:
        raise RuntimeError(f"{node_id}: no pitch windows returned data across the Statcast era")


# ---------------------------------------------------------------------------
# Specs
# ---------------------------------------------------------------------------

# Named without the `_SPECS` suffix so `load_nodes()` does NOT discover them
# directly — see leaderboards.py. The canonical `baseball_savant.py` aggregates.
STATCAST_DOWNLOADS = [
    NodeSpec(id=f"{SLUG}-statcast-pitches", fn=fetch_statcast_pitches, kind="download"),
]

STATCAST_TRANSFORMS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in STATCAST_DOWNLOADS
]
