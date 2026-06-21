"""Post-DAG health invariants for the PDET microdata connector.

Each entity writes its raw as a set of per-batch `ndjson.gz` assets
(`<spec_id>-<batch_key>.ndjson.gz`), so we discover them via the glob the SQL
transform uses, not a single fixed asset id.
"""

from subsets_utils import list_raw_files


def test_every_entity_has_raw_batches(spec_ids):
    """Each download spec must have produced at least one batch file. None means
    discovery returned nothing or the FTP/extract path broke silently."""
    for sid in spec_ids:
        files = list_raw_files(f"{sid}-*")
        assert files, f"{sid}: no raw batch files (.ndjson.gz) found"


def test_raw_batches_are_ndjson(spec_ids):
    """Batches must be the ndjson.gz the transform can read — a wrong extension
    means a writer regression that would break the SQL view."""
    for sid in spec_ids:
        files = list_raw_files(f"{sid}-*")
        bad = [f for f in files if not f.lower().endswith(".ndjson.gz")]
        assert not bad, f"{sid}: non-ndjson raw files present: {bad[:5]}"
