"""Post-DAG health invariants for the UN Comtrade connector.

The single download spec (`un-comtrade-values`) writes one parquet batch per
year named `un-comtrade-values-<year>`, so we discover batches by glob rather
than loading the bare spec id.
"""
from subsets_utils import list_raw_files, load_raw_parquet


def _batch_assets() -> list[str]:
    # raw/un-comtrade-values-<year>.parquet -> asset id "un-comtrade-values-<year>"
    return [
        f.removesuffix(".parquet")
        for f in list_raw_files("un-comtrade-values-*.parquet")
    ]


def test_many_year_batches():
    """One batch per annual period; ~35 expected. A handful means the crawl
    barely started or the availability list collapsed."""
    batches = _batch_assets()
    assert len(batches) >= 20, (
        f"only {len(batches)} year batches; expected >=20"
    )


def test_batches_nonempty_and_typed():
    """Each batch must hold rows with the expected trade columns - guards
    against an endpoint format switch silently writing empty/garbage parquet."""
    batches = _batch_assets()
    required = {
        "refYear", "reporterCode", "partnerCode",
        "flowDesc", "primaryValue", "cmdCode",
    }
    total = 0
    for asset in batches:
        table = load_raw_parquet(asset)
        assert len(table) > 0, f"{asset}: 0 rows"
        missing = required - set(table.column_names)
        assert not missing, f"{asset}: missing columns {missing}"
        total += len(table)
    # ~3M+ rows across the full matrix; a small total means truncation.
    assert total >= 500_000, f"only {total:,} total raw rows across batches"


def test_flows_and_total_only():
    """Every row should be a TOTAL-commodity Import/Export record; anything
    else means the query params drifted."""
    batches = _batch_assets()
    # Sample a few batches to keep the test cheap.
    for asset in sorted(batches)[:5]:
        table = load_raw_parquet(asset)
        flows = set(table.column("flowDesc").to_pylist())
        assert flows <= {"Import", "Export"}, f"{asset}: unexpected flows {flows}"
        cmds = set(table.column("cmdCode").to_pylist())
        assert cmds == {"TOTAL"}, f"{asset}: non-TOTAL cmdCodes {cmds}"
