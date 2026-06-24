"""Post-DAG health invariants for the ENTSOG raw assets.

Every download node writes NDJSON via subsets_utils.save_raw_ndjson. operationaldata
writes one batch per month (`<id>-YYYY-MM`); the others write a single file named
after the spec id. We load through the same loader and assert the raw actually
holds rows — catching silent empties (format switch, auth/endpoint drift) that
mere file existence would miss.
"""
from subsets_utils import load_raw_ndjson, list_raw_files

OPERATIONALDATA = "entsog-transparency-platform-operationaldata"
_EXTS = (".ndjson.zst", ".ndjson.gz", ".ndjson")


def _asset_id(rel_path: str) -> str:
    """Strip the raw dir prefix and NDJSON extension to recover the asset id."""
    name = rel_path.split("raw/")[-1]
    for ext in _EXTS:
        if name.endswith(ext):
            return name[: -len(ext)]
    return name


def test_simple_assets_nonempty(spec_ids):
    """Each single-file download asset should hold rows."""
    for sid in spec_ids:
        if sid == OPERATIONALDATA:
            continue  # batched — checked below
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw NDJSON has 0 rows"


def test_operationaldata_batches_nonempty(spec_ids):
    """operationaldata is written as monthly batches; batches must exist and the
    union must hold rows (a few empty/404 months are fine)."""
    if OPERATIONALDATA not in spec_ids:
        return
    batches = list_raw_files(f"{OPERATIONALDATA}-*")
    assert batches, f"{OPERATIONALDATA}: no monthly batch files written"
    total = sum(len(load_raw_ndjson(_asset_id(b))) for b in batches)
    assert total > 0, f"{OPERATIONALDATA}: all {len(batches)} monthly batches empty"
