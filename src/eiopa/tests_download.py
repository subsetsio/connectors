"""Health invariants for EIOPA raw assets — catch silent degradation
(empty payloads, truncated downloads, wrong shape) that file-existence misses."""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec must have written at least one raw NDJSON row.
    An empty payload usually means the S3 file moved/renamed or the xlsx
    sheet name changed silently."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw NDJSON has 0 rows"


def test_value_fields_present(spec_ids):
    """Spot-check that the value-bearing column for each asset family is present
    in the raw records — guards against a header/sheet drift that drops the
    measure column."""
    for sid in spec_ids:
        sample = load_raw_ndjson(sid)[0]
        if sid == "eiopa-solo-asset-exposures":
            assert "value_eur_millions" in sample, f"{sid}: missing value_eur_millions"
        elif sid == "eiopa-financial-stability-indicators":
            assert "median" in sample, f"{sid}: missing median"
        else:
            assert "value" in sample and "item_code" in sample, \
                f"{sid}: missing value/item_code ({sorted(sample)})"
