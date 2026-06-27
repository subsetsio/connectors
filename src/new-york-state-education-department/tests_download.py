"""Post-DAG health invariants for the NYSED connector.

Each subset is one Access table converted to a gzipped NDJSON raw asset. These
tests catch silent degradation that file-existence alone misses: an empty payload
(mdbtools found no matching table, or the source changed the table name), or a
malformed conversion (rows without the injected report_year). We stream a bounded
prefix of each asset rather than loading multi-million-row tables fully.
"""
import json

from subsets_utils import raw_reader


def _first_rows(spec_id, limit=200):
    rows = []
    with raw_reader(spec_id, "ndjson.gz", mode="rt", compression="gzip") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
            if len(rows) >= limit:
                break
    return rows


def test_all_raw_assets_nonempty(spec_ids):
    """Every subset's raw asset must contain at least one record. An empty file
    means mdb-export matched no table (renamed/removed) or every year was skipped."""
    empty = []
    for sid in spec_ids:
        if not _first_rows(sid, limit=1):
            empty.append(sid)
    assert not empty, f"{len(empty)} subset(s) produced empty raw assets: {empty}"


def test_report_year_present_and_sane(spec_ids):
    """report_year is injected on every row from the source file's school year;
    it must be an int in a plausible range. A missing/garbage value means the
    conversion path broke."""
    bad = []
    for sid in spec_ids:
        for rec in _first_rows(sid, limit=200):
            y = rec.get("report_year")
            if not isinstance(y, int) or not (1995 <= y <= 2027):
                bad.append((sid, y))
                break
    assert not bad, f"rows with missing/implausible report_year: {bad[:10]}"
