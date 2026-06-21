"""Health-invariant tests for the TSA connector raw assets."""
import datetime as _dt

from subsets_utils import load_raw_parquet


def test_raw_nonempty_and_full_span(spec_ids):
    """The daily throughput series spans 2019-01-01 to ~now. If we got far
    fewer rows than ~6 years of days, a year page silently failed to parse or
    the table format changed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        n = len(table)
        assert n >= 2000, f"{sid}: only {n} rows; expected >=2000 (~6+ years daily)"

        dates = table.column("date").to_pylist()
        assert min(dates) <= _dt.date(2019, 1, 1), (
            f"{sid}: earliest date {min(dates)} > 2019-01-01 — backfill years missing"
        )
        # Latest row should be recent (source updates Mon-Fri); allow slack.
        assert max(dates) >= _dt.date(2024, 1, 1), (
            f"{sid}: latest date {max(dates)} is stale — current year page not scraped"
        )


def test_passengers_plausible(spec_ids):
    """Daily national throughput is millions per day (post-2020) but dipped to
    ~90k at the 2020 trough. Catch a units/format break (e.g. commas not
    stripped → tiny ints, or a stray header row)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        vals = table.column("passengers").to_pylist()
        assert all(isinstance(v, int) for v in vals), f"{sid}: non-int passenger values"
        assert min(vals) > 1000, f"{sid}: min passengers {min(vals)} implausibly low"
        assert max(vals) < 5_000_000, f"{sid}: max passengers {max(vals)} implausibly high"


def test_dates_unique(spec_ids):
    """One row per calendar date; duplicates mean the base/year-page union
    failed to dedup."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        dates = table.column("date").to_pylist()
        assert len(dates) == len(set(dates)), f"{sid}: duplicate dates in raw asset"
