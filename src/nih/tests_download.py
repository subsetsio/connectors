"""Post-run health invariants for the NIH ExPORTER connector.

Each download spec writes one NDJSON.gz batch per year as a separate raw asset
(`<spec>-<year>`); the transform unions them via the `<spec>-*` rule. We check
batch coverage and that a sample batch holds keyed rows — catching silent
degradation (truncated listing, empty/format-shifted files) that mere file
existence would miss.

Enumeration goes through the COMMITTED raw manifest (`dep_fragments`), the same
commit-log the transforms read — NOT a physical run-scoped directory glob. The
glob proved unreliable against R2 at finalize (it returned zero batches for a
spec whose 40+ files were demonstrably committed), while the manifest is the
live truth for exactly the files the transform will see.
"""

from subsets_utils import load_raw_ndjson, raw_manifest

# Each per-year group spans ~40 years; allow headroom but trip if the manifest
# silently references only a handful of batches.
_MIN_BATCHES = 30

# Raw columns are normalized to UPPER_SNAKE in the fetch fn.
_KEY_COLUMN = {
    "nih-project": "APPLICATION_ID",
    "nih-abstract": "APPLICATION_ID",
    "nih-publication": "PMID",
}

_NDJSON_SUFFIXES = (".ndjson.gz", ".ndjson", ".jsonl.gz", ".jsonl")


def _batch_asset_ids(sid):
    """This spec's year-batch asset ids (e.g. 'nih-project-2025') per the
    committed raw manifest — manifest-truth, run-dir agnostic."""
    frags = raw_manifest.dep_fragments(sid) or []
    ids = []
    for ref, _uri in frags:
        name = ref.rsplit("/", 1)[-1]
        for suffix in _NDJSON_SUFFIXES:
            if name.endswith(suffix):
                ids.append(name[: -len(suffix)])
                break
    return sorted(set(ids))


def test_each_spec_has_year_batches(spec_ids):
    for sid in spec_ids:
        ids = _batch_asset_ids(sid)
        assert len(ids) >= _MIN_BATCHES, (
            f"{sid}: only {len(ids)} yearly batch assets in the raw manifest "
            f"(expected >= {_MIN_BATCHES}); listing likely truncated"
        )


def test_sample_batch_nonempty_and_keyed(spec_ids):
    for sid in spec_ids:
        ids = _batch_asset_ids(sid)
        assert ids, f"{sid}: no batch assets in the raw manifest"
        asset = ids[-1]  # most recent year
        rows = load_raw_ndjson(asset)
        assert rows, f"{asset}: raw NDJSON batch has 0 rows"
        key = _KEY_COLUMN[sid]
        present = sum(1 for r in rows[:1000] if r.get(key) not in (None, ""))
        assert present > 0, (
            f"{asset}: key column {key!r} empty across sampled rows — "
            "source format may have shifted"
        )
