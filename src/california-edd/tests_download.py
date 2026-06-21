"""Health-invariant tests for the California EDD connector.

Each raw asset is a gzip-compressed NDJSON dump (one CSV row per line, keyed by
the source's CSV headers). We stream-read the head of each file rather than
loading whole multi-million-row dumps into memory: enough to prove the payload
is non-empty, valid JSON, and carries the expected EDD header shape (an
'Area ...' or 'Date' column) — which catches the silent-degradation modes
(empty payload, truncated download, format switch, auth wall returning HTML).
"""

import json

from subsets_utils import raw_reader


def _first_rows(sid, n=5):
    rows = []
    with raw_reader(sid, "ndjson.gz", mode="rt", compression="gzip") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
            if len(rows) >= n:
                break
    return rows


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw NDJSON must have at least one parseable row."""
    download_ids = [s for s in spec_ids if not s.endswith("-transform")]
    for sid in download_ids:
        rows = _first_rows(sid, n=1)
        assert rows, f"{sid}: raw ndjson.gz has 0 rows"


def test_rows_are_json_objects_with_columns(spec_ids):
    """First rows must be JSON objects with multiple columns — guards against a
    truncated/HTML body that happens to gunzip but isn't the expected CSV."""
    download_ids = [s for s in spec_ids if not s.endswith("-transform")]
    for sid in download_ids:
        rows = _first_rows(sid, n=3)
        for r in rows:
            assert isinstance(r, dict), f"{sid}: row is not a JSON object: {r!r:.120}"
            assert len(r) >= 2, f"{sid}: row has <2 columns: {sorted(r)}"


def test_expected_edd_geography_or_date_column(spec_ids):
    """Every EDD table is keyed by geography ('Area ...') and/or a date/period.
    Absence across all sampled rows means the header changed upstream."""
    download_ids = [s for s in spec_ids if not s.endswith("-transform")]
    for sid in download_ids:
        rows = _first_rows(sid, n=5)
        keys = set().union(*(r.keys() for r in rows)) if rows else set()
        lowered = {k.lower() for k in keys}
        has_signal = any(
            k.startswith("area ") or k in ("date", "year", "period", "filed week ended")
            for k in lowered
        )
        assert has_signal, f"{sid}: no Area/Date/Year/Period column found in {sorted(keys)}"
