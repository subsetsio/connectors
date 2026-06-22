"""Health-invariant tests — run post-DAG, in-connector, against the raw assets.

Covers both single-file assets (competitions, matches) and per-match batch assets
(events, lineups, three_sixty), which are written as `<spec_id>-<match_id>.parquet`.
"""

from subsets_utils import list_raw_files, load_raw_parquet

# Assets written as one file per match (batch layout) vs a single exact-named file.
BATCHED = {"statsbomb-events", "statsbomb-lineups", "statsbomb-three-sixty"}


def test_raw_assets_present_and_nonempty(spec_ids):
    for sid in spec_ids:
        if sid in BATCHED:
            files = list_raw_files(f"{sid}-*.parquet")
            assert files, f"{sid}: no per-match batch parquet files written"
        else:
            files = list_raw_files(f"{sid}.parquet")
            assert files, f"{sid}: raw parquet missing"


def test_single_file_assets_have_rows(spec_ids):
    for sid in ("statsbomb-competitions", "statsbomb-matches"):
        if sid not in spec_ids:
            continue
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_batched_assets_have_rows(spec_ids):
    """At least one batch file per batched asset must carry rows — an all-empty
    asset means the per-match fetch silently returned nothing."""
    import pyarrow.parquet as pq
    from subsets_utils.io import raw_uri

    for sid in BATCHED:
        if sid not in spec_ids:
            continue
        rels = list_raw_files(f"{sid}-*.parquet")
        assert rels, f"{sid}: no batch files"
        total = 0
        for rel in rels[:50]:  # sample the first batches; enough to prove non-empty
            asset_id = rel[: -len(".parquet")]
            total += load_raw_parquet(asset_id).num_rows
        assert total > 0, f"{sid}: first {min(len(rels),50)} batch files all empty"
