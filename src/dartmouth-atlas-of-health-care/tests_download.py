"""Health-invariant tests for the Dartmouth Atlas connector.

Raw assets are gzipped NDJSON, some of them multi-GB / tens of millions of rows,
so we STREAM each asset with raw_reader and inspect a bounded prefix rather than
materializing the whole file (load_raw_ndjson would OOM the big topics)."""

import json

from subsets_utils import raw_reader

# Required keys per raw asset shape.
_TOPIC_KEYS = {"geo_level", "geo_code", "year", "measure_code", "adjusted_rate"}
_CROSSWALK_KEYS = {"zipcode", "hsa_num", "hrr_num", "vintage"}

_SAMPLE = 5000  # rows to inspect from the head of each asset


def _head(spec_id, n=_SAMPLE):
    rows = []
    with raw_reader(spec_id, "ndjson.gz", mode="rt", compression="gzip") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
            if len(rows) >= n:
                break
    return rows


def test_all_raw_assets_nonempty(spec_ids):
    """Every download asset must hold at least one record. An empty NDJSON
    usually means the zip layout changed or every file 404'd silently."""
    for sid in spec_ids:
        rows = _head(sid, n=1)
        assert rows, f"{sid}: raw NDJSON has 0 rows"


def test_expected_keys_present(spec_ids):
    """Each asset's rows must carry the canonical keys its transform reads.
    A missing key means the normalizer drifted from the source headers."""
    for sid in spec_ids:
        rows = _head(sid, n=50)
        assert rows, f"{sid}: no rows to check keys"
        keys = set(rows[0].keys())
        wanted = _CROSSWALK_KEYS if sid.endswith("geography-crosswalk") else _TOPIC_KEYS
        missing = wanted - keys
        assert not missing, f"{sid}: rows missing expected keys {sorted(missing)}"


def test_topic_year_plausible(spec_ids):
    """Topic rows should carry 4-digit years within the Atlas era. Catches a
    column-misalignment that puts a non-year value into `year`."""
    for sid in spec_ids:
        if sid.endswith("geography-crosswalk"):
            continue
        years = [r.get("year") for r in _head(sid) if r.get("year") is not None]
        assert years, f"{sid}: no non-null years in sample"
        assert all(1990 <= int(y) <= 2026 for y in years), (
            f"{sid}: implausible years in sample (min={min(years)}, max={max(years)})"
        )


def test_crosswalk_zip_shape(spec_ids):
    """Crosswalk ZIPs must be 5-char zero-padded strings (leading zeros kept)."""
    for sid in spec_ids:
        if not sid.endswith("geography-crosswalk"):
            continue
        zips = [r.get("zipcode") for r in _head(sid)]
        assert zips, f"{sid}: no rows"
        bad = [z for z in zips if not (isinstance(z, str) and len(z) == 5 and z.isdigit())]
        assert not bad, f"{sid}: {len(bad)} malformed zipcodes (e.g. {bad[:3]})"
