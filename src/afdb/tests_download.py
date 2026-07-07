"""Post-DAG health invariants for the AfDB connector.

Catches silent degradation that file-existence alone misses: a Cloudflare
bounce that wrote an empty file, a schema that lost its date/value columns, a
dataset that came back with no observations.
"""

from subsets_utils import list_raw_files, load_raw_ndjson

# A couple of genuinely small datasets (hbubefg ~21 series, salbpsf ~52) we can
# fully load without risking OOM on the big ones (nbyenxf has ~5M rows).
SMALL_ASSETS = ["afdb-hbubefg", "afdb-salbpsf"]


def test_every_asset_has_a_raw_file(spec_ids):
    """Each download node must have written a raw ndjson.gz. A missing file
    means the fetch crashed before writing (often a Cloudflare 403 that
    exhausted retries)."""
    for sid in spec_ids:
        files = list_raw_files(f"{sid}.ndjson*")
        assert files, f"{sid}: no raw file written"


def test_small_assets_well_formed(spec_ids):
    """For the small datasets we can afford to load fully: rows exist and carry
    the universal long-format columns. Guards against a schema regression in
    the expansion step."""
    for sid in SMALL_ASSETS:
        if sid not in spec_ids:
            continue
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"
        cols = set(rows[0])
        assert {"date", "value", "frequency"} <= cols, (
            f"{sid}: missing core columns; got {sorted(cols)}"
        )
        assert all(r.get("value") is not None for r in rows[:1000]), (
            f"{sid}: null values leaked into raw (expansion should drop them)"
        )
