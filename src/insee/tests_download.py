"""Post-DAG health invariants for the INSEE connector.

Runs in-connector after the download nodes, seeing raw through subsets_utils
loaders. Catches silent degradation file-existence alone misses: a datacube
that returned an empty/format-changed payload, or rows missing the value column.
"""

from subsets_utils import list_raw_files, load_raw_ndjson

# A few intentionally small datacubes — deep-checked without loading the
# multi-million-row assets (DS_FLORES_*, DS_RP_*, DS_PRENOM) into memory.
_SAMPLE = [
    "insee-ds-erfs-champ-const-sl",
    "insee-ds-srcv-pms",
    "insee-ds-tice",
    "insee-ds-erfs-individu",
]


def test_all_raw_assets_present(spec_ids):
    """Every download spec must have written its NDJSON raw asset. A missing
    file means the fetch silently produced nothing."""
    missing = [sid for sid in spec_ids if not list_raw_files(f"{sid}.*")]
    assert not missing, f"{len(missing)} specs wrote no raw file: {missing[:10]}"


def test_sample_assets_have_observations(spec_ids):
    """Small sample datacubes must hold rows whose flattened records carry the
    measure value, its measure name, and the TIME_PERIOD dimension — the
    columns the transform depends on."""
    checked = 0
    for sid in _SAMPLE:
        if sid not in spec_ids:
            continue
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw NDJSON has 0 rows"
        row = rows[0]
        for col in ("OBS_VALUE", "OBS_MEASURE", "TIME_PERIOD"):
            assert col in row, f"{sid}: row missing '{col}' (got {sorted(row)[:12]})"
        assert any(r.get("OBS_VALUE") is not None for r in rows), \
            f"{sid}: every observation has a null OBS_VALUE"
        checked += 1
    assert checked > 0, "no sample asset was present among spec_ids to deep-check"
