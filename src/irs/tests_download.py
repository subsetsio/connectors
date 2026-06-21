"""Health invariants for the IRS connector raw assets.

Each download spec writes one parquet *batch* per source file (year / state /
direction) under `<spec-id>-<batch_key>`, so we glob `<spec-id>-*` rather than
loading an exact asset name.
"""

from subsets_utils import list_raw_files, load_raw_parquet


def _batches(sid: str) -> list[str]:
    """Asset ids (no extension) of the parquet batches for one spec."""
    return [
        f[: -len(".parquet")]
        for f in list_raw_files(f"{sid}-*")
        if f.endswith(".parquet")
    ]


def test_every_spec_produced_batches(spec_ids):
    """A spec with zero batch files means discovery found nothing — the URL
    scheme changed or every probe 404'd."""
    for sid in spec_ids:
        assert _batches(sid), f"{sid}: no parquet batch files discovered"


def test_batches_nonempty_and_uniform(spec_ids):
    """Every batch must hold rows, and all batches of a spec must share one
    schema (positional multi-file read in the transform depends on it)."""
    for sid in spec_ids:
        batches = _batches(sid)
        assert batches, f"{sid}: no batches"
        ref_schema = None
        total = 0
        # cap at a handful of batches to keep the test fast on big programs
        for asset in batches[:8]:
            table = load_raw_parquet(asset)
            assert table.num_rows > 0, f"{sid}: batch {asset} has 0 rows"
            total += table.num_rows
            if ref_schema is None:
                ref_schema = table.schema
            else:
                assert table.schema.equals(ref_schema), (
                    f"{sid}: batch {asset} schema diverges from siblings"
                )
        assert total > 0, f"{sid}: all sampled batches empty"
