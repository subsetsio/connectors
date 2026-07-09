"""Health invariants for the BLS bulk flat-file download assets.

These catch the silent degradations that file existence alone misses: a survey whose
observation files vanished from the directory listing, a value column that stopped
parsing (BLS pads every field with spaces — one missed `trim` turns every value into
NULL), the 403-on-bad-UA quirk yielding an HTML error body, and a series-catalog join
that dropped out and left a published table of bare ids.
"""
from subsets_utils import load_raw_parquet

# Every survey's asset carries these, whatever its own dimension columns are.
_CORE_COLS = {"series_id", "year", "period", "period_start_date", "value", "footnote_codes"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every survey asset must hold observation rows. Empty usually means the
    listing parse failed or the endpoint returned an HTML error body."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_core_columns_present(spec_ids):
    """The 5-column observation schema plus our derived date is stable across surveys."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = _CORE_COLS - cols
        assert not missing, f"{sid}: raw parquet missing core columns {sorted(missing)}"


def test_values_parsed(spec_ids):
    """`value` is space-padded numeric text in the source; a failed cast nulls the column."""
    for sid in spec_ids:
        col = load_raw_parquet(sid).column("value")
        assert col.null_count < len(col), f"{sid}: every `value` is null — the cast failed"


def test_series_ids_trimmed(spec_ids):
    """BLS pads series_id to a fixed width; untrimmed ids join to nothing downstream."""
    for sid in spec_ids:
        ids = load_raw_parquet(sid).column("series_id").to_pylist()[:1000]
        bad = [s for s in ids if not s or s != s.strip()]
        assert not bad, f"{sid}: {len(bad)} series_id values are empty or whitespace-padded"


def test_series_catalog_joined(spec_ids):
    """Each asset carries dimension columns from `<survey>.series`, and they matched.

    A silently-failed catalog join leaves every row present but every dimension null —
    the survey keeps its numbers and loses its meaning.
    """
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        dims = [c for c in table.column_names if c not in _CORE_COLS]
        assert dims, f"{sid}: no dimension columns — the series-catalog join produced nothing"
        joined = any(table.column(c).null_count < len(table) for c in dims)
        assert joined, f"{sid}: every dimension column is null — the catalog join matched no rows"
