"""Health-invariant tests for BioTIME raw assets — catch silent degradation
(empty payloads, truncated unzips, wrong format) that file-existence misses."""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_records_is_large(spec_ids):
    """The records corpus should hold millions of rows; a partial unzip or a
    stream that died early would land far short."""
    if "biotime-records" in spec_ids:
        table = load_raw_parquet("biotime-records")
        assert len(table) >= 1_000_000, f"biotime-records only {len(table)} rows"


def test_records_has_expected_columns(spec_ids):
    if "biotime-records" in spec_ids:
        cols = set(load_raw_parquet("biotime-records").column_names)
        for c in ("study_id", "year", "abundance", "genus_species"):
            assert c in cols, f"biotime-records missing column {c}: {sorted(cols)}"


def test_studies_one_row_per_study(spec_ids):
    if "biotime-studies" in spec_ids:
        table = load_raw_parquet("biotime-studies")
        assert "study_id" in table.column_names, "biotime-studies missing study_id"
        n = len(table)
        assert 300 <= n <= 1000, f"biotime-studies has {n} rows; expected ~381"
