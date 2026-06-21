"""Health invariants for the GDELT download stage.

Raw is written as one immutable parquet batch per GDELT file-date
(gdelt-events-YYYY-MM-DD.parquet), each holding pre-aggregated
(event_day x action-country x event-root x quad) groups. We discover the batch
files with list_raw_files and load a sample through the same parquet loader the
download node used. A batch may legitimately span a few event-days (late-detected
stragglers), so we do NOT assert a single date per batch."""
from subsets_utils import list_raw_files, load_raw_parquet

_ASSET = "gdelt-events"
_EXPECTED_COLS = {
    "date", "action_geo_country_iso2", "event_root_code", "quad_class",
    "num_events", "sum_mentions", "sum_articles", "sum_goldstein", "sum_tone",
}


def _batch_asset_ids():
    files = list_raw_files(f"{_ASSET}-*.parquet")
    return sorted(f[: -len(".parquet")] for f in files)


def test_batches_exist():
    """At least one file-date must have been processed; zero batches means the
    crawl wrote nothing (master list parse broke, or every file 404'd)."""
    ids = _batch_asset_ids()
    assert ids, f"no batch files matched {_ASSET}-*.parquet"


def test_batches_nonempty_and_well_formed():
    """Each sampled batch holds positive event counts, valid quad classes, and
    two-digit CAMEO root codes. Catches truncated downloads and schema drift."""
    ids = _batch_asset_ids()
    sample = ids[:3] + ids[-3:]
    for sid in sample:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: empty batch"
        cols = set(table.column_names)
        assert _EXPECTED_COLS <= cols, f"{sid}: missing columns ({_EXPECTED_COLS - cols})"

        quads = set(table.column("quad_class").to_pylist())
        assert quads <= {1, 2, 3, 4}, f"{sid}: unexpected quad_class values {quads}"

        n = table.column("num_events").to_pylist()
        assert all(c > 0 for c in n), f"{sid}: non-positive num_events present"

        roots = set(table.column("event_root_code").to_pylist())
        assert all(len(r) == 2 and r.isdigit() for r in roots), f"{sid}: bad event_root_code {roots}"


def test_iso_country_codes_present():
    """Most events resolve to an ISO country; if a sampled batch is entirely
    null-country the FIPS->ISO mapping silently broke."""
    ids = _batch_asset_ids()
    sample = ids[:3] + ids[-3:]
    for sid in sample:
        table = load_raw_parquet(sid)
        countries = table.column("action_geo_country_iso2").to_pylist()
        non_null = [c for c in countries if c]
        assert non_null, f"{sid}: every row has null action_geo_country_iso2 (FIPS map broke?)"
