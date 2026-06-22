from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataset's raw NDJSON should hold observation rows. An empty payload
    means the series listing or observations batch came back empty (format/auth
    change) rather than failing loudly."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_core_columns_present(spec_ids):
    """Each row must carry the series key, a period, and a value — the three
    fields the transform depends on."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[0]
        for col in ("series", "period", "value"):
            assert col in sample, f"{sid}: row missing {col!r} column"


def test_values_mostly_present(spec_ids):
    """Observations should carry numeric values; an all-null asset means the
    value field moved or the endpoint shape changed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        non_null = sum(1 for r in rows if r.get("value") is not None)
        assert non_null > 0, f"{sid}: every observation value is null"
