"""Health-invariant tests for the Gun Violence Archive raw download.

These run post-DAG, in-connector, against the raw parquet the download node
wrote — catching silent degradation (Cloudflare block returning an empty/HTML
body, a report's markup changing so a population drops out, pagination clamping
early) that file existence alone misses.
"""

from subsets_utils import load_raw_parquet

_EXPECTED_COLS = {
    "incident_id", "incident_date", "state", "city_or_county", "address",
    "victims_killed", "victims_injured", "suspects_killed", "suspects_injured",
    "suspects_arrested", "report_population", "report_name",
}


def test_raw_nonempty(spec_ids):
    """Every standing report contributes incidents; a near-empty corpus means
    Cloudflare blocked us or the export-api markup changed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows >= 2000, (
            f"{sid}: only {table.num_rows} rows; expected several thousand "
            f"across ~11 standing reports"
        )


def test_raw_schema(spec_ids):
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = _EXPECTED_COLS - cols
        assert not missing, f"{sid}: missing columns {missing}"


def test_report_populations_present(spec_ids):
    """We discover and crawl ~11 standing reports; if discovery degraded
    (a slug stopped embedding its UUID) the distinct population count drops."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        pops = set(table.column("report_population").to_pylist())
        assert len(pops) >= 8, (
            f"{sid}: only {len(pops)} report populations present ({sorted(pops)}); "
            f"expected >=8 — report discovery likely degraded"
        )


def test_casualty_counts_sane(spec_ids):
    """Casualty counts are non-negative small integers; negatives or absurd
    magnitudes mean a column shifted during HTML parsing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        vk = [v for v in table.column("victims_killed").to_pylist() if v is not None]
        assert vk, f"{sid}: victims_killed all null"
        assert min(vk) >= 0, f"{sid}: negative victims_killed {min(vk)}"
        assert max(vk) < 1000, f"{sid}: implausible victims_killed {max(vk)} (column shift?)"
