"""Health-invariant tests for the nd-gain raw assets.

Catch silent degradation that file-existence alone misses: empty payloads
(scrape returned a page with no ZIP link, or the ZIP layout changed) and
wrong-shape parquet (a CSV format change upstream).
"""

from subsets_utils import load_raw_parquet

EXPECTED_COLS = {
    "nd-gain-gain": {"iso3", "country", "year", "score"},
    "nd-gain-vulnerability": {"iso3", "country", "year", "category", "score"},
    "nd-gain-readiness": {"iso3", "country", "year", "category", "score"},
    "nd-gain-indicators": {
        "iso3", "country", "year", "indicator_id",
        "raw_value", "input_value", "score_value",
    },
    "nd-gain-trends": {"iso3", "country", "measure", "value", "sign"},
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw asset should hold rows. Empty usually means the scrape
    found no ZIP link or the archive structure changed under us."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_columns(spec_ids):
    """Each raw asset must carry exactly the columns its transform reads; a
    missing/renamed column means the upstream CSV header drifted."""
    for sid in spec_ids:
        if sid not in EXPECTED_COLS:
            continue
        cols = set(load_raw_parquet(sid).column_names)
        missing = EXPECTED_COLS[sid] - cols
        assert not missing, f"{sid}: missing expected columns {sorted(missing)}"
