"""Health invariants for the Bank of Italy raw assets.

Each raw asset is the gzipped ndjson of one BDS table's PROSPETTODATI
observations, stamped with the canonical `table_id` / `series_id` / `date` /
`value` columns on top of the table's native shape.

The per-node YAML specs assert content (coverage, freshness, uniqueness) in
DuckDB. These catch what lives above the data: a node that "succeeded" without
writing, and the ragged-schema failure that made an earlier version of this
connector unreadable — DuckDB infers an NDJSON schema from a leading sample, so
a column appearing only in later rows never binds in the transform.
"""

import gzip
import json

from subsets_utils import list_raw_files

_CANONICAL = {"table_id", "series_id", "date", "value"}


def _raw_path(spec_id):
    matches = list_raw_files("%s.ndjson.gz" % spec_id)
    assert matches, "%s: no raw file written" % spec_id
    return matches[0]


def test_every_spec_wrote_raw(spec_ids):
    """A download node that returns without writing is a silent hole."""
    for sid in spec_ids:
        _raw_path(sid)


def test_first_row_carries_full_schema(spec_ids):
    """Row 1 must name every column the file uses.

    The fetch fn fills each row out to the table's column union, so row 1 is the
    schema. If a later row introduces a key row 1 lacks, inference from the
    leading sample would drop that column and the transform's binding would fail.
    """
    for sid in spec_ids:
        with gzip.open(_raw_path(sid), "rt") as fh:
            first = fh.readline()
            assert first, "%s: raw file is empty" % sid
            keys = set(json.loads(first))
            missing = _CANONICAL - keys
            assert not missing, "%s: missing canonical columns %s" % (sid, sorted(missing))
            for _ in range(200):
                line = fh.readline()
                if not line:
                    break
                extra = set(json.loads(line)) - keys
                assert not extra, "%s: row adds columns absent from row 1: %s" % (sid, sorted(extra))


def test_values_are_numeric(spec_ids):
    """Some row must carry a numeric `value`.

    A table whose every value is null means the payload came back as status
    codes or dates only — the format break that a null-fraction threshold on any
    single table would not localise.
    """
    for sid in spec_ids:
        found = False
        with gzip.open(_raw_path(sid), "rt") as fh:
            for _ in range(500):
                line = fh.readline()
                if not line:
                    break
                if json.loads(line).get("value") is not None:
                    found = True
                    break
        assert found, "%s: no numeric value in first 500 rows" % sid
