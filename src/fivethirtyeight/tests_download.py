from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every CSV should parse to a non-empty table. An empty/0-row asset means
    the raw fetch 404'd, returned an error page, or the CSV failed to parse."""
    empties = []
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if len(table) == 0 or table.num_columns == 0:
            empties.append(sid)
    assert not empties, f"{len(empties)} assets empty/columnless: {empties[:10]}"


def test_assets_have_columns(spec_ids):
    """A FiveThirtyEight CSV always has a header row -> >=1 column. Zero columns
    would mean we saved an error blob, not a CSV."""
    bad = [sid for sid in spec_ids if load_raw_parquet(sid).num_columns < 1]
    assert not bad, f"{len(bad)} assets have no columns: {bad[:10]}"
