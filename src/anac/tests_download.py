"""Health invariants for the ANAC raw downloads, run post-DAG in-connector.

Each subset's raw is a set of per-file shards (`<spec_id>.sNNNNN.ndjson.gz`) that
the transform globs and unions. The streaming read of the first non-empty shard
catches the common silent failures — empty payload, truncated/format-switched
download — without loading potentially multi-GB assets (airfares, VRA) fully
into memory.
"""
from subsets_utils import list_raw_files, raw_reader

_NDJSON_SUFFIX = ".ndjson.gz"


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        files = list_raw_files(f"{sid}.*")
        assert files, f"{sid}: no raw shard written"

        nonempty = False
        for rel in files:
            name = rel.rsplit("/", 1)[-1]
            assert name.endswith(_NDJSON_SUFFIX), f"{sid}: unexpected raw file {rel!r}"
            asset = name[: -len(_NDJSON_SUFFIX)]
            with raw_reader(asset, "ndjson.gz", mode="rt", compression="gzip") as f:
                if f.readline().strip():
                    nonempty = True
                    break
        assert nonempty, f"{sid}: every raw shard is empty"
