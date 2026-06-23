"""Post-DAG health invariants for the EBA connector raw assets.

These catch silent degradation that file-existence alone misses: an empty
payload (page renamed, scrape matched nothing), a truncated download, or the
KRI sheet losing its expected columns.
"""

from subsets_utils import load_raw_parquet

KRI_ID = "eba-risk-dashboard-kri"
TE_IDS = [
    "eba-te-credit-risk",
    "eba-te-market-risk",
    "eba-te-sovereign-exposures",
    "eba-te-other-exposures",
]


def test_all_raw_assets_nonempty(spec_ids):
    """Every EBA raw asset must hold rows — empty means discovery/scrape or the
    download silently failed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_kri_schema(spec_ids):
    """The Risk Dashboard KRI asset must carry its tidy long-format columns."""
    if KRI_ID not in spec_ids:
        return
    table = load_raw_parquet(KRI_ID)
    expected = {"period", "country", "indicator_code", "indicator_name", "value"}
    assert expected.issubset(set(table.column_names)), (
        f"{KRI_ID}: columns {table.column_names} missing {expected}"
    )
    # Several countries + the EU/EEA aggregate should be present.
    n_countries = len(set(table.column("country").to_pylist()))
    assert n_countries >= 20, f"{KRI_ID}: only {n_countries} distinct countries"


def test_te_assets_have_core_columns(spec_ids):
    """Transparency Exercise CSVs must keep their long-format keys."""
    for sid in TE_IDS:
        if sid not in spec_ids:
            continue
        cols = set(load_raw_parquet(sid).column_names)
        for c in ("LEI_Code", "NSA", "Period", "Item", "Amount"):
            assert c in cols, f"{sid}: missing column {c}; have {sorted(cols)}"
