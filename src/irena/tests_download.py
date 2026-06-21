"""Health-invariant tests for the IRENA raw assets.

These run post-DAG, in-connector, reading raw via the same loader the download
node used (save_raw_parquet -> load_raw_parquet). They catch silent degradation
that file-existence alone misses: empty/truncated tables, a year chunk that
quietly dropped, or a dimension column vanishing after a cycle change.
"""

from subsets_utils import load_raw_parquet

# Required columns we publish per asset (the normalized dimension names).
_REQUIRED_COLS = {
    "irena-country-eleccap": {"year", "country", "technology", "grid_connection", "value"},
    "irena-country-elecgen": {"year", "country", "technology", "data_type", "grid_connection", "value"},
    "irena-heatgen": {"year", "country", "technology", "grid_connection", "value"},
    "irena-pubfin": {"year", "country", "technology", "value"},
    "irena-re-share": {"year", "region", "indicator", "value"},
    "irena-region-eleccap": {"year", "region", "technology", "grid_connection", "value"},
    "irena-region-elecgen": {"year", "region", "technology", "data_type", "value"},
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every table must hold rows. An empty payload means the year-chunked POST
    loop produced nothing — format/endpoint change or auth failure."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_required_columns_present(spec_ids):
    """Each asset must carry its expected dimension columns; a missing one means
    a dimension dropped or the metadata parse changed."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        required = _REQUIRED_COLS.get(sid)
        assert required is not None, f"{sid}: unexpected spec id"
        missing = required - cols
        assert not missing, f"{sid}: missing columns {missing} (have {cols})"


def test_multiple_years_present(spec_ids):
    """Each table is a long historical series; if year chunking silently broke
    after one chunk we'd see a single year. Expect a broad span."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        years = set(table.column("year").to_pylist())
        assert len(years) >= 10, f"{sid}: only {len(years)} distinct years ({sorted(years)})"


def test_values_finite(spec_ids):
    """Values should be real numbers — no NaN/inf leaking from a parse error."""
    import math

    for sid in spec_ids:
        table = load_raw_parquet(sid)
        for v in table.column("value").to_pylist():
            assert v is not None and math.isfinite(v), f"{sid}: non-finite value {v}"
            break  # one check per asset is enough to catch a systemic parse break
