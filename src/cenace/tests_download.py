"""Health invariants for the CENACE raw assets.

Raw is written as date-windowed batches named ``<spec_id>-<system>-<market>-<window>``,
so we look for batch files via the glob and load one to confirm it carries rows
with the expected price columns. Empty/absent batches usually mean the web
service changed format or every window was treated as 'no data'.
"""

from subsets_utils import list_raw_files, load_raw_parquet

# spec_id -> a price column that must be present and (mostly) populated.
_PRICE_COL = {
    "cenace-pml": "pml",
    "cenace-pend": "pz",
    "cenace-psc": "pres",
}


def test_each_product_has_batches(spec_ids):
    for sid in spec_ids:
        files = list_raw_files(f"{sid}-*.parquet")
        assert files, f"{sid}: no raw batch files written"


def test_batches_nonempty_and_priced(spec_ids):
    for sid in spec_ids:
        files = sorted(list_raw_files(f"{sid}-*.parquet"))
        assert files, f"{sid}: no raw batch files"
        # The batch asset id is the filename stem (minus .parquet).
        asset = files[0].rsplit("/", 1)[-1][: -len(".parquet")]
        table = load_raw_parquet(asset)
        assert len(table) > 0, f"{sid}: batch {asset} has 0 rows"
        col = _PRICE_COL[sid]
        assert col in table.column_names, f"{sid}: batch missing price column '{col}'"
        nonnull = sum(1 for v in table.column(col).to_pylist() if v is not None)
        assert nonnull > 0, f"{sid}: price column '{col}' is entirely null in {asset}"
