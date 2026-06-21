"""Health-invariant tests for IOM raw assets.

Catch silent degradation that file-existence alone misses: a WAF serving an
HTML error page as "csv", a truncated download, an upstream that emptied out.
"""
from subsets_utils import load_raw_parquet

# Loose floors well under observed volumes (DTM ~234k rows, MM ~22k rows) so
# normal growth never trips them, but a truncated/empty payload does.
MIN_ROWS = {
    "iom-dtm-displacement": 100_000,
    "iom-missing-migrants": 15_000,
}


def test_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_raw_assets_meet_minimum_rows(spec_ids):
    for sid in spec_ids:
        floor = MIN_ROWS.get(sid)
        if floor is None:
            continue
        n = len(load_raw_parquet(sid))
        assert n >= floor, f"{sid}: {n} rows < expected floor {floor} (truncated download?)"


def test_dtm_key_columns_present(spec_ids):
    if "iom-dtm-displacement" not in spec_ids:
        return
    cols = set(load_raw_parquet("iom-dtm-displacement").column_names)
    for c in ("admin0_name", "num_present_idp_ind", "reporting_date"):
        assert c in cols, f"iom-dtm-displacement: missing raw column {c}"


def test_mm_key_columns_present(spec_ids):
    if "iom-missing-migrants" not in spec_ids:
        return
    cols = set(load_raw_parquet("iom-missing-migrants").column_names)
    for c in ("main_id", "incident_date", "total_dead_and_missing"):
        assert c in cols, f"iom-missing-migrants: missing raw column {c}"
