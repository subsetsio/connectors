"""Health invariants for the BCEAO download nodes — catch silent degradation
(empty payloads, a frequency or locality silently dropping out, the export
format shifting) that mere file-existence checks would miss."""

from subsets_utils import load_raw_parquet


def test_values_nonempty_and_shaped(spec_ids):
    if "bceao-values" not in spec_ids:
        return
    t = load_raw_parquet("bceao-values")
    assert t.num_rows > 100_000, f"bceao-values has only {t.num_rows} rows"
    cols = set(t.column_names)
    for c in ("series_code", "value", "date", "locality", "frequency", "country"):
        assert c in cols, f"bceao-values missing column {c}"
    freqs = set(t.column("frequency").to_pylist()[:200000])
    assert {"A", "M"} <= freqs, f"expected at least annual+monthly; saw {sorted(freqs)}"


def test_values_multiple_localities(spec_ids):
    if "bceao-values" not in spec_ids:
        return
    t = load_raw_parquet("bceao-values")
    locs = set(t.column("locality").to_pylist())
    assert len(locs) >= 5, f"expected several localities, saw {sorted(locs)}"


def test_series_catalog_nonempty(spec_ids):
    if "bceao-series" not in spec_ids:
        return
    t = load_raw_parquet("bceao-series")
    assert t.num_rows > 1000, f"bceao-series has only {t.num_rows} rows"
    sectors = set(t.column("sector").to_pylist())
    assert {"SR", "SF", "SE"} <= sectors, f"missing core sectors; saw {sorted(sectors)}"
