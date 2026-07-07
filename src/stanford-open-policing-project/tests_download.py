"""Bounded health checks for OPP raw downloads.

The largest location files contain millions of rows, so these tests inspect raw
file presence and the first NDJSON record instead of loading whole assets into
memory.
"""

import json

from subsets_utils import list_raw_files, raw_reader

_SUFFIX = ".ndjson.gz"


def test_every_spec_wrote_ndjson(spec_ids):
    for sid in spec_ids:
        files = list_raw_files(f"{sid}.*")
        assert files, f"{sid}: no raw files written"
        assert any(path.endswith(_SUFFIX) for path in files), (
            f"{sid}: expected an {_SUFFIX} raw file, got {files}"
        )


def test_first_record_has_provenance_and_date(spec_ids):
    for sid in spec_ids:
        files = [path for path in list_raw_files(f"{sid}.*") if path.endswith(_SUFFIX)]
        assert files, f"{sid}: no NDJSON file written"
        asset = files[0].rsplit("/", 1)[-1][: -len(_SUFFIX)]
        with raw_reader(asset, "ndjson.gz", mode="rt", compression="gzip") as handle:
            first = handle.readline().strip()
        assert first, f"{sid}: NDJSON file is empty"
        row = json.loads(first)
        for column in ("_source_entity_id", "_source_file", "_row_number", "date"):
            assert row.get(column) is not None, f"{sid}: first row missing {column}"
