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

from datetime import datetime, timezone, timedelta, date
import gzip

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_file, list_raw_files

from utils import SLUG, STATCAST_ERA_START_YEAR, _fetch_csv_text

# statcast_search hard-caps any query at 25,000 rows. A full MLB day is ~3,000-5,500
# pitches, so a 3-day window (~16k worst case) stays comfortably under the cap.
STATCAST_ROW_CAP = 25000
STATCAST_WINDOW_DAYS = 3

# MLB activity (spring training → World Series) spans roughly March–November; the
# Dec/Jan/Feb offseason has no Statcast pitches. Walking only these months drops
# ~1/4 of windows that would otherwise be wasted empty requests every leg.
STATCAST_SEASON_FIRST_MONTH = 3   # March (spring training onset)
STATCAST_SEASON_LAST_MONTH = 11   # November (World Series tail)


def _season_windows(start_year: int, end: date):
    """Yield (win_start, win_end) 3-day windows over the MLB-season months of
    every year start_year..end.year, each window clipped to `end`. Off-season
    months are skipped entirely so no request is spent on them."""
    for year in range(start_year, end.year + 1):
        season_start = date(year, STATCAST_SEASON_FIRST_MONTH, 1)
        season_end = min(date(year, STATCAST_SEASON_LAST_MONTH, 30), end)
        if season_start > end:
            break
        cur = season_start
        while cur <= season_end:
            win_end = min(cur + timedelta(days=STATCAST_WINDOW_DAYS - 1), season_end)
            yield cur, win_end
            cur = win_end + timedelta(days=1)


# ---------------------------------------------------------------------------
# Statcast pitch-by-pitch (date-windowed, resumable full re-pull)
# ---------------------------------------------------------------------------
# Raw is run-scoped in this harness (runs/<run_id>/raw/...) while state is durable
# across runs, so a *cross-run* watermark would let a later run skip fetching yet
# land its raw in a fresh, empty scope. The corpus is therefore re-pulled in full
# every *run*. But the ~960-window era walk does not fit in one 355-min job, so a
# run is split across continuation legs that all share this run's RUN_ID — hence
# its raw scope. Each leg lists the windows already saved in that shared scope and
# skips them (`list_raw_files`), fetching only the un-downloaded tail. Progress is
# therefore monotonic across legs: a leg that runs out of budget mid-walk is
# resumed by the next leg from where raw leaves off, and once every window is
# present the download returns immediately so the transform leg gets a full budget.

def fetch_statcast_pitches(node_id: str) -> None:
    end = datetime.now(timezone.utc).date()

    # Windows already saved in this run's (leg-shared) raw scope — skip them so a
    # continuation leg only fetches the tail the prior legs didn't reach.
    already = set(list_raw_files(f"{node_id}-*.csv.gz"))
    n_have = len(already)
    n_new = 0

    for cur, win_end in _season_windows(STATCAST_ERA_START_YEAR, end):
        fname = f"{node_id}-{win_end.isoformat()}.csv.gz"
        if fname in already:
            continue
        url = (
            "https://baseballsavant.mlb.com/statcast_search/csv?all=true&type=details"
            f"&player_type=pitcher&game_date_gt={cur.isoformat()}"
            f"&game_date_lt={win_end.isoformat()}"
        )
        text = _fetch_csv_text(url)
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
            n_new += 1

    # Raise only when the run scope ends up empty (no pre-existing windows AND
    # nothing newly fetched) — NOT when a continuation leg found everything
    # already downloaded (n_have > 0, n_new == 0), which is the success path.
    if n_have == 0 and n_new == 0:
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
