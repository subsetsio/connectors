"""Health invariants for the OPEC MOMR-appendix raw assets.

Catch silent degradation the file-exists check misses: a workbook whose layout
drifted (header row no longer found -> 0 rows), a sheet that collapsed to a
single series/period, or the period classifier breaking (no recognised
frequencies).
"""

from subsets_utils import load_raw_parquet

_EXPECTED_COLS = {
    "report_period", "report_date", "table", "table_title",
    "section", "item", "period", "frequency", "period_start", "value",
}


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        t = load_raw_parquet(sid)
        assert t.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_columns(spec_ids):
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = _EXPECTED_COLS - cols
        assert not missing, f"{sid}: missing columns {missing}"


def test_shape_not_degenerate(spec_ids):
    """Each sheet is a real cross-section: many series across several periods.
    A drop to ~1 series or ~1 period means the grid parse silently broke."""
    for sid in spec_ids:
        t = load_raw_parquet(sid).to_pydict()
        n_items = len(set(t["item"]))
        n_periods = len(set(t["period"]))
        assert n_items >= 5, f"{sid}: only {n_items} distinct items (parse degraded?)"
        assert n_periods >= 4, f"{sid}: only {n_periods} distinct periods (parse degraded?)"


def test_frequencies_recognised(spec_ids):
    """Every row must carry a known frequency; the classifier emitting an
    unexpected token signals a header-format change."""
    allowed = {"annual", "quarterly", "monthly"}
    for sid in spec_ids:
        freqs = set(load_raw_parquet(sid).to_pydict()["frequency"])
        assert freqs and freqs <= allowed, f"{sid}: unexpected frequencies {freqs - allowed}"


def test_multiple_vintages(spec_ids):
    """We accumulate several monthly report vintages — if only one resolved,
    discovery (URL probing) probably degraded."""
    for sid in spec_ids:
        vintages = set(load_raw_parquet(sid).to_pydict()["report_period"])
        assert len(vintages) >= 3, f"{sid}: only {len(vintages)} report vintage(s)"
