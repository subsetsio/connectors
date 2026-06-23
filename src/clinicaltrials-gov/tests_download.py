"""Health invariants for the ClinicalTrials.gov raw assets.

Reads each node's ndjson.gz with a STREAMING reader (raw_reader) rather than
load_raw_ndjson — `locations` is several million rows and must not be pulled
fully into memory just to count it.
"""
import gzip
import json

from subsets_utils import raw_reader

NCT_PREFIX = "NCT"

# Minimum rows we expect per asset given ~590K studies in the registry. Loose
# enough for normal growth/variation, tight enough that a pagination break
# (stops after page 1 → ~1000 studies) trips the assertion.
MIN_ROWS = {
    "clinicaltrials-gov-studies": 400_000,
    "clinicaltrials-gov-conditions": 400_000,
    "clinicaltrials-gov-interventions": 200_000,
    "clinicaltrials-gov-outcome-measures": 300_000,
    "clinicaltrials-gov-sponsors-collaborators": 400_000,
    "clinicaltrials-gov-locations": 300_000,
}


def _iter_rows(sid):
    with raw_reader(sid, "ndjson.gz", mode="rb") as fh:
        with gzip.open(fh, mode="rt", encoding="utf-8") as g:
            for line in g:
                line = line.strip()
                if line:
                    yield json.loads(line)


def test_all_raw_assets_meet_min_rows(spec_ids):
    """Every asset must hold at least its expected floor of rows. A tiny count
    means pagination broke after page 1 or the projection returned nothing."""
    for sid in spec_ids:
        floor = MIN_ROWS.get(sid, 1)
        n = 0
        first = None
        for row in _iter_rows(sid):
            if first is None:
                first = row
            n += 1
            if n >= floor:
                break  # floor satisfied; no need to count the rest
        assert n >= floor, f"{sid}: only {n} rows; expected >= {floor}"
        assert first and first.get("nct_id"), f"{sid}: first row missing nct_id: {first}"


def test_nct_ids_well_formed(spec_ids):
    """nct_id should look like NCT followed by 8 digits across a sample of rows.
    Malformed ids mean the projection or flattening drifted."""
    for sid in spec_ids:
        checked = 0
        for row in _iter_rows(sid):
            nct = row.get("nct_id")
            assert isinstance(nct, str) and nct.startswith(NCT_PREFIX) and nct[3:].isdigit() and len(nct) == 11, (
                f"{sid}: malformed nct_id {nct!r}"
            )
            checked += 1
            if checked >= 5000:
                break
        assert checked > 0, f"{sid}: no rows to validate"
