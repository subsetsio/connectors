"""Post-DAG health invariants for the Freightos Baltic Index connector."""
from subsets_utils import load_raw_parquet

# The public FBX family carried by the FBX Full Data sheet.
EXPECTED_CODES = {"FBX", "FBX01", "FBX03", "FBX11", "FBX13"}


def test_raw_nonempty(spec_ids):
    """Each spec's raw asset must hold rows. An empty payload means the embed
    stopped resolving or the live-data sheet changed shape silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_index_codes(spec_ids):
    """The known FBX index family must be present. A missing code means the
    sheet header drifted or parsing dropped a column."""
    table = load_raw_parquet("freightos-baltic-index-values")
    codes = set(table.column("index_code").to_pylist())
    missing = EXPECTED_CODES - codes
    assert not missing, f"missing FBX index codes: {missing} (got {codes})"


def test_history_depth(spec_ids):
    """~153 weekly observations per code (2023-04 -> present). A near-empty
    grid means the live-data fetch degraded."""
    table = load_raw_parquet("freightos-baltic-index-values")
    n = len(table)
    assert n >= 500, f"only {n} long-format rows; expected >=500 (>=100 weeks x 5 codes)"


def test_values_mostly_present(spec_ids):
    """Currency parsing should yield numeric values for the vast majority of
    cells. A flood of nulls means the cell format changed."""
    table = load_raw_parquet("freightos-baltic-index-values")
    vals = table.column("value").to_pylist()
    nonnull = [v for v in vals if v is not None and v > 0]
    assert len(nonnull) >= 0.9 * len(vals), (
        f"only {len(nonnull)}/{len(vals)} parsed to positive numbers"
    )
