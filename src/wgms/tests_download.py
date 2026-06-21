"""Post-download health invariants for the WGMS connector."""

from subsets_utils import list_raw_files, load_raw_parquet


def test_every_spec_wrote_raw(spec_ids):
    """Each download spec must leave at least one raw file. Missing raw means
    the release URL stopped resolving or the zip member vanished."""
    for sid in spec_ids:
        files = list_raw_files(f"{sid}.*") or list_raw_files(f"{sid}-*")
        assert files, f"{sid}: no raw files written"


def test_fog_tables_nonempty():
    """The flagship FoG parquet tables must hold rows — an empty parquet means
    the CSV member was misnamed or the stream broke silently."""
    for sid in (
        "wgms-fog-glacier",
        "wgms-fog-mass-balance",
        "wgms-fog-front-variation",
        "wgms-fog-change",
    ):
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_fog_glacier_is_global():
    """The glacier register should list many thousands of glaciers across many
    countries — a tiny count means a truncated download."""
    table = load_raw_parquet("wgms-fog-glacier")
    assert len(table) >= 10_000, f"wgms-fog-glacier: only {len(table)} rows"


def test_amce_glacier_covers_many_regions():
    """amce_glacier is written as one ndjson batch per GTN-G region; far fewer
    than ~19 batches means region discovery or the unpivot broke."""
    files = list_raw_files("wgms-amce-glacier-*")
    assert len(files) >= 15, (
        f"wgms-amce-glacier: expected >=15 region batches, got {len(files)}"
    )
