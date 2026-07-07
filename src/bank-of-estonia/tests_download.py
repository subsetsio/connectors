"""Health invariants for the Bank of Estonia raw assets.

Each download node writes a long-format parquet (period, date, series, value).
These catch silent degradation: empty payloads (endpoint switched format or the
report went non-public), and dates/values that all failed to parse (number/date
format drift)."""
from subsets_utils import load_raw_parquet


def _raw_spec_ids(spec_ids):
    return [sid for sid in spec_ids if not sid.endswith("-transform")]


def test_all_raw_assets_nonempty(spec_ids):
    """Every report we kept is public + has-data, so its parsed long table must
    hold rows. Zero rows means the CSV came back empty or the matrix parser
    failed to recognise the layout."""
    empties = []
    raw_ids = _raw_spec_ids(spec_ids)
    for sid in raw_ids:
        try:
            t = load_raw_parquet(sid)
        except Exception as e:  # noqa: BLE001 - surface which asset + error class
            empties.append(f"{sid} (load error: {type(e).__name__})")
            continue
        if t.num_rows == 0:
            empties.append(f"{sid} (0 rows)")
    assert not empties, f"{len(empties)}/{len(raw_ids)} raw assets empty/unreadable: {empties[:15]}"


def test_dates_mostly_parsed(spec_ids):
    """Across all assets, the vast majority of rows must carry a parsed ISO date.
    A high null-date rate means a period-label format the parser doesn't cover."""
    total = 0
    dated = 0
    for sid in _raw_spec_ids(spec_ids):
        t = load_raw_parquet(sid)
        if t.num_rows == 0:
            continue
        total += t.num_rows
        col = t.column("date").to_pylist()
        dated += sum(1 for d in col if d)
    assert total > 0, "no rows across any asset"
    assert dated >= 0.9 * total, f"only {dated}/{total} rows have a parsed date (<90%)"


def test_values_are_numeric(spec_ids):
    """Values must be real floats, not all-null — guards against a parser that
    silently drops every cell (e.g. a number-format change)."""
    nonnull = 0
    for sid in _raw_spec_ids(spec_ids):
        t = load_raw_parquet(sid)
        if t.num_rows == 0:
            continue
        nonnull += sum(1 for v in t.column("value").to_pylist() if v is not None)
    assert nonnull > 0, "every value across every asset is null"
