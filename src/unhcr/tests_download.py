"""Health invariants for the UNHCR raw downloads."""
from subsets_utils import load_raw_ndjson

# Endpoints that break down by country should have far more than a handful of
# rows (full origin x asylum x year grid). nowcasting is national-only.
_MIN_ROWS = {
    "unhcr-population": 50000,
    "unhcr-asylum-applications": 50000,
    "unhcr-asylum-decisions": 30000,
    "unhcr-demographics": 5000,
    "unhcr-solutions": 1000,
    "unhcr-idmc": 100,
    "unhcr-unrwa": 50,
    "unhcr-nowcasting": 1,
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every endpoint's NDJSON must hold rows; empty means format/auth drift."""
    for sid in _raw_spec_ids(spec_ids):
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_row_counts_plausible(spec_ids):
    """Per-endpoint floor catches pagination silently stopping after page 1
    (which would cap a country-breakdown endpoint near 20000)."""
    for sid in _raw_spec_ids(spec_ids):
        floor = _MIN_ROWS.get(sid)
        if floor is None:
            continue
        n = len(load_raw_ndjson(sid))
        assert n >= floor, f"{sid}: {n} rows < expected floor {floor}"


def test_year_column_present(spec_ids):
    """Every record must carry an integer year — the core dimension."""
    for sid in _raw_spec_ids(spec_ids):
        rows = load_raw_ndjson(sid)
        sample = rows[0]
        assert "year" in sample, f"{sid}: no 'year' field in records"
        assert isinstance(sample["year"], int), f"{sid}: year not int: {sample['year']!r}"


def _raw_spec_ids(spec_ids):
    """The full DAG can pass transform ids too; health checks target raw only."""
    return [sid for sid in spec_ids if not sid.endswith("-transform")]
