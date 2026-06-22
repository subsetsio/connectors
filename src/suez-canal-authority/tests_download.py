"""Post-DAG health invariants for suez-canal-authority raw assets."""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every report must decode to rows. An empty payload means the Power BI
    querydata call failed silently or the DSR decoder broke."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_no_all_null_rows(spec_ids):
    """A decoded row should carry at least one non-null value; an all-null row
    signals the R/Ø bitmask decoding drifted out of alignment."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        empty = [i for i, r in enumerate(rows) if not any(v is not None for v in r.values())]
        assert not empty, f"{sid}: {len(empty)} all-null rows (DSR decode misaligned)"


def test_year_columns_plausible(spec_ids):
    """Wherever a year column exists, values sit in a sane canal-era range —
    catches a column-name mismap or a units/decoding error."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        for col in ("year", "Year"):
            if rows and col in rows[0]:
                years = [r[col] for r in rows if isinstance(r.get(col), int)]
                assert years, f"{sid}: no integer values in {col}"
                assert min(years) >= 1950 and max(years) <= 2100, \
                    f"{sid}: {col} out of range [{min(years)}, {max(years)}]"
