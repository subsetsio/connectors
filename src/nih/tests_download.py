"""Post-run health invariants for the NIH ExPORTER connector.

Each download spec writes one NDJSON.gz batch per year (`<spec>-<year>`), so we
check batch coverage and that a sample batch holds rows with its key column —
catching silent degradation (truncated listing, empty/again-format-shifted files)
that mere file existence would miss.
"""

from subsets_utils import list_raw_files, load_raw_ndjson

# Each per-year group spans ~40 years; allow headroom but trip if a listing
# silently truncated to a handful of files.
_MIN_BATCHES = 30

_KEY_COLUMN = {
    "nih-project": "application_id",
    "nih-abstract": "application_id",
    "nih-publication": "pmid",
}


def _asset_id(rel_path: str) -> str:
    name = rel_path.split("/")[-1]
    for suffix in (".ndjson.gz", ".ndjson", ".jsonl.gz", ".jsonl"):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return name


def test_each_spec_has_year_batches(spec_ids):
    for sid in spec_ids:
        batches = list_raw_files(f"{sid}-*")
        assert len(batches) >= _MIN_BATCHES, (
            f"{sid}: only {len(batches)} yearly batch files "
            f"(expected >= {_MIN_BATCHES}); listing likely truncated"
        )


def test_sample_batch_nonempty_and_keyed(spec_ids):
    for sid in spec_ids:
        batches = sorted(list_raw_files(f"{sid}-*"))
        assert batches, f"{sid}: no batch files found"
        asset = _asset_id(batches[-1])  # most recent year
        rows = load_raw_ndjson(asset)
        assert rows, f"{asset}: raw NDJSON batch has 0 rows"
        key = _KEY_COLUMN[sid]
        upper = key.upper()
        present = sum(1 for r in rows[:1000] if r.get(upper) not in (None, ""))
        assert present > 0, (
            f"{asset}: key column {upper!r} empty across sampled rows — "
            "source format may have shifted"
        )
