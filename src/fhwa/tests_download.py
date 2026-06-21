"""Post-DAG health invariants for the FHWA download nodes.

Each raw asset is the full NDJSON export of one Socrata dataset. These guard
against silent degradation: an endpoint that switched format or auth-expired
returns an empty/truncated payload, and a dataset losing its key columns means
the schema drifted upstream.
"""

from subsets_utils import load_raw_ndjson

# Minimum row counts observed during probing (well below live counts, so normal
# growth never trips them but a truncated/empty pull does).
_MIN_ROWS = {
    "fhwa-54nx-se7f": 100,    # ~125 (annual, 1900-present)
    "fhwa-hvfw-tcmn": 3000,   # ~3825 (state x year, 1950-present)
    "fhwa-ix2d-bsqq": 10000,  # ~16575 (state x year x revenue source)
    "fhwa-mt5m-skz3": 200,    # ~310 (state x year)
    "fhwa-taz8-hut2": 50,     # ~68 (fiscal year)
}

_KEY_FIELDS = {
    "fhwa-54nx-se7f": ["year", "vmt"],
    "fhwa-hvfw-tcmn": ["year", "state", "gallons"],
    "fhwa-ix2d-bsqq": ["year", "state", "revenues", "dollars"],
    "fhwa-mt5m-skz3": ["year", "state"],
    "fhwa-taz8-hut2": ["fiscal_year", "receipts"],
}


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw NDJSON has 0 rows"


def test_row_counts_plausible(spec_ids):
    for sid in spec_ids:
        floor = _MIN_ROWS.get(sid)
        if floor is None:
            continue
        rows = load_raw_ndjson(sid)
        assert len(rows) >= floor, f"{sid}: {len(rows)} rows < expected floor {floor}"


def test_key_fields_present(spec_ids):
    """At least one row of each dataset must carry its key fields — catches a
    silent upstream schema rename."""
    for sid in spec_ids:
        fields = _KEY_FIELDS.get(sid)
        if fields is None:
            continue
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: no rows to check fields on"
        for f in fields:
            present = any(f in r for r in rows[:200])
            assert present, f"{sid}: key field '{f}' missing from sampled rows"
