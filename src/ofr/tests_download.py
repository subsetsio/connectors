"""Health-invariant tests — run post-DAG, in-connector, against the raw assets.

Catch silent degradation that file-existence misses: empty payloads, truncated
downloads, a dataset endpoint quietly changing shape.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw parquet must hold rows."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_dataset_long_format_columns(spec_ids):
    """The 9 long-format dataset assets must expose (mnemonic, date, value)."""
    special = {"ofr-fsi", "ofr-ofr-series-catalog"}
    for sid in spec_ids:
        if sid in special:
            continue
        cols = set(load_raw_parquet(sid).column_names)
        assert {"mnemonic", "date", "value"} <= cols, f"{sid}: missing long-format cols, got {cols}"


def test_fsi_shape(spec_ids):
    """FSI raw must be the wide stress-index table with the headline column."""
    if "ofr-fsi" not in spec_ids:
        return
    t = load_raw_parquet("ofr-fsi")
    cols = set(t.column_names)
    assert {"date", "ofr_fsi", "credit", "volatility"} <= cols, f"ofr-fsi cols: {cols}"
    assert len(t) >= 6000, f"ofr-fsi only {len(t)} rows; expected daily history since 2000"


def test_series_catalog_unique(spec_ids):
    """Catalog must have unique mnemonics across both monitors."""
    if "ofr-ofr-series-catalog" not in spec_ids:
        return
    t = load_raw_parquet("ofr-ofr-series-catalog")
    mnemonics = t.column("mnemonic").to_pylist()
    assert len(mnemonics) == len(set(mnemonics)), "ofr-series-catalog has duplicate mnemonics"
    assert len(mnemonics) >= 800, f"catalog only {len(mnemonics)} series"
