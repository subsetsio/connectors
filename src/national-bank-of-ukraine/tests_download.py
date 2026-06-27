"""Health-invariant tests for the NBU connector raw assets.

Some assets are single files (`<sid>.ndjson.zst`); the windowed / FX assets are
batched (`<sid>-<YYYYMM>...` / `<sid>-<YYYY>...`). Both layouts are discovered
the same way the SQL transform discovers them.
"""

from subsets_utils import list_raw_files, load_raw_ndjson

_EXTS = (".ndjson.zst", ".ndjson.gz", ".ndjson")


def _asset_ids_for(sid):
    """Return the raw asset ids (no extension) backing one download spec —
    the single exact-name file if present, else the batch files."""
    rels = list_raw_files(f"{sid}.*") or list_raw_files(f"{sid}-*")
    ids = []
    for rel in rels:
        for ext in _EXTS:
            if rel.endswith(ext):
                ids.append(rel[: -len(ext)])
                break
    return ids


def test_every_spec_has_raw(spec_ids):
    """Each download node must have produced at least one ndjson raw file."""
    missing = [sid for sid in spec_ids if not _asset_ids_for(sid)]
    assert not missing, f"no raw ndjson files for: {missing}"


def test_raw_assets_nonempty(spec_ids):
    """Raw files must hold records — an empty payload usually means the endpoint
    changed format or Cloudflare started blocking us."""
    for sid in spec_ids:
        ids = _asset_ids_for(sid)
        if not ids:
            continue
        total = sum(len(load_raw_ndjson(aid)) for aid in ids)
        assert total > 0, f"{sid}: raw present but 0 records across {len(ids)} file(s)"


def test_records_have_expected_keys(spec_ids):
    """statdirectory records carry dt + id_api + value; FX records carry
    cc + exchangedate + rate. A schema drift trips this."""
    for sid in spec_ids:
        ids = _asset_ids_for(sid)
        if not ids:
            continue
        rows = load_raw_ndjson(ids[0])
        if not rows:
            continue
        keys = set(rows[0].keys())
        if sid.endswith("official-exchange-rates"):
            need = {"cc", "exchangedate", "rate"}
        else:
            need = {"dt", "id_api", "value"}
        assert need <= keys, f"{sid}: expected keys {need} not all present in {sorted(keys)}"
