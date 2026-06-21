"""Health invariants for the ABS SDMX downloads.

Each download writes one dataflow's full SDMX-CSV as NDJSON. These tests catch
silent degradation that file-existence alone misses: empty payloads, a response
that switched away from SDMX-CSV (losing the stable OBS_VALUE/TIME_PERIOD
columns), or a dataflow that returned only non-numeric observations.
"""
from subsets_utils import load_raw_ndjson, list_raw_files

# Columns SDMX-CSV always carries regardless of the dataflow's DSD.
_STABLE_COLS = {"DATAFLOW", "TIME_PERIOD", "OBS_VALUE"}


def test_every_asset_has_rows(spec_ids):
    """Every download that produced a raw asset must hold at least one row.
    An empty NDJSON usually means the endpoint switched format or the flow was
    silently withdrawn."""
    for sid in spec_ids:
        if not list_raw_files(sid):
            # Permanent 4xx (superseded dataflow) skips cleanly with no raw —
            # that is an accepted per-entity outcome, not a degradation.
            continue
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: NDJSON has 0 rows"


def test_stable_sdmx_columns_present(spec_ids):
    """The SDMX-CSV stable columns must be present on the first row of every
    asset — their absence means the response was not the expected flat table."""
    for sid in spec_ids:
        if not list_raw_files(sid):
            continue
        rows = load_raw_ndjson(sid)
        if not rows:
            continue
        cols = set(rows[0].keys())
        missing = _STABLE_COLS - cols
        assert not missing, f"{sid}: missing stable SDMX columns {missing}"


def test_some_numeric_observations(spec_ids):
    """At least one asset must carry a parseable numeric OBS_VALUE — guards
    against a corpus-wide format break where everything becomes non-numeric."""
    saw_numeric = False
    for sid in spec_ids:
        if not list_raw_files(sid):
            continue
        rows = load_raw_ndjson(sid)
        for r in rows[:200]:
            v = (r.get("OBS_VALUE") or "").strip()
            if v:
                try:
                    float(v)
                    saw_numeric = True
                    break
                except ValueError:
                    continue
        if saw_numeric:
            break
    assert saw_numeric, "no parseable numeric OBS_VALUE found across any asset"
