"""Health invariants for the Bank of Italy raw assets.

Each raw asset is the gzipped ndjson of one BDS table's PROSPETTODATI
observations, stamped with the canonical `table_id` / `series_id` / `date` /
`value` columns on top of the table's native shape.

The per-node YAML specs assert content (coverage, freshness, uniqueness, null
fractions) in DuckDB, which streams. What is left for here is what lives above
the data: a node that "succeeded" without writing anything, and the two shape
breaks that would make a table load but be wrong — losing the canonical columns,
or returning a payload of dates and status codes with no numeric value at all.

Content checks run over a deterministic sample: `load_raw_ndjson` materialises a
whole table, and TRI30021 alone is ~1.8M observations.
"""

import random

from subsets_utils import list_raw_files, load_raw_ndjson

_CANONICAL = {"table_id", "series_id", "date", "value"}
_SAMPLE = 20


def _sample(spec_ids):
    ids = sorted(spec_ids)
    return ids if len(ids) <= _SAMPLE else random.Random(0).sample(ids, _SAMPLE)


def test_every_spec_wrote_raw(spec_ids):
    """A download node that returns without writing is a silent hole."""
    for sid in spec_ids:
        assert list_raw_files("%s.ndjson.gz" % sid), "%s: no raw file written" % sid


def test_sampled_assets_are_well_formed(spec_ids):
    """Sampled tables hold rows, expose the canonical columns, and carry values.

    The fetch fn fills every row out to the table's column union, so row 1 names
    every column the file uses; a later row that adds one would mean the fill was
    bypassed, and DuckDB — which infers an NDJSON schema from a leading sample —
    would silently drop that column at transform time.
    """
    for sid in _sample(spec_ids):
        rows = load_raw_ndjson(sid)
        assert rows, "%s: raw ndjson has 0 observations" % sid

        keys = set(rows[0])
        missing = _CANONICAL - keys
        assert not missing, "%s: missing canonical columns %s" % (sid, sorted(missing))

        for row in rows:
            extra = set(row) - keys
            assert not extra, "%s: row adds columns absent from row 1: %s" % (sid, sorted(extra))

        assert any(r["value"] is not None for r in rows), (
            "%s: every observation has a null value - the payload returned no numbers" % sid
        )
