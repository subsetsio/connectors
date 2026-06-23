"""Health invariants for the INEI download nodes -- catch silent degradation
(empty payloads, truncated crawls, format switches) that file existence misses."""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every download node must produce rows. An empty payload usually means the
    SIRTOD servlet returned an error page or `null` instead of a JSON array."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_indicators_catalog_large(spec_ids):
    """arboltematico exposed ~6940 indicators; a small catalog means the tree
    parse silently dropped leaves or pagination/format changed."""
    if "inei-indicators" not in spec_ids:
        return
    table = load_raw_parquet("inei-indicators")
    assert len(table) >= 4000, f"indicators catalog only {len(table)} rows; expected >=4000"


def test_annual_values_substantial(spec_ids):
    """The annual values table is the flagship; a thin table means most batches
    came back empty (poisoned indicador_listado or year window collapsed)."""
    if "inei-values-annual" not in spec_ids:
        return
    table = load_raw_parquet("inei-values-annual")
    assert len(table) >= 30000, f"annual values only {len(table)} rows; expected >=30000"
    ind = set(table.column("indicador_id").to_pylist())
    assert len(ind) >= 2000, f"annual values cover only {len(ind)} indicators; expected >=2000"


def test_monthly_has_month_columns(spec_ids):
    """Monthly raw is wide: indicador_id, anio, m1..m12. A missing month column
    means the dato_mensual response shape changed."""
    if "inei-values-monthly" not in spec_ids:
        return
    table = load_raw_parquet("inei-values-monthly")
    names = set(table.column_names)
    for m in range(1, 13):
        assert f"m{m}" in names, f"monthly raw missing column m{m}"
