"""Health invariants for the Bank of England download — catch silent
degradation that file existence alone misses (empty payloads, format drift,
the HTML-error-as-HTTP-200 trap that yields a parseable-but-wrong file)."""
from subsets_utils import load_raw_parquet

_ASSET = "bank-of-england-values"
_EXPECTED = {"series_code", "series_title", "obs_date", "value"}


def test_values_nonempty_and_well_formed():
    """The observations asset must hold rows with the expected schema. Zero
    rows or missing columns usually mean the IADB endpoint switched format or
    returned its HTML error page instead of CSV."""
    table = load_raw_parquet(_ASSET)
    assert table.num_rows > 0, f"{_ASSET}: raw parquet has 0 rows"
    assert _EXPECTED.issubset(set(table.column_names)), (
        f"{_ASSET}: columns {table.column_names} missing some of {_EXPECTED}"
    )


def test_series_codes_present_and_diverse():
    """Every row carries a series code, and the pull spans many distinct series
    (not a single-series degenerate fetch)."""
    table = load_raw_parquet(_ASSET)
    codes = table.column("series_code").to_pylist()
    assert all(c for c in codes), f"{_ASSET}: null/empty series_code present"
    assert len(set(codes)) >= 100, (
        f"{_ASSET}: only {len(set(codes))} distinct series — discovery degraded"
    )


def test_values_mostly_numeric():
    """Stored values must parse as numbers for the vast majority of rows. A
    sudden wall of non-numeric text means footnote/format contamination."""
    table = load_raw_parquet(_ASSET)
    vals = table.column("value").to_pylist()
    numeric = 0
    for v in vals:
        if v is None:
            continue
        try:
            float(v)
            numeric += 1
        except (TypeError, ValueError):
            pass
    assert numeric >= 0.95 * len(vals), (
        f"{_ASSET}: only {numeric}/{len(vals)} values are numeric"
    )
