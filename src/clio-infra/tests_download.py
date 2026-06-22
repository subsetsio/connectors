"""Health invariants for Clio Infra raw assets, run post-DAG in-connector."""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every indicator file is a non-empty global time series. An empty raw
    asset means the XLSX changed format, the 'Data Long Format' sheet vanished,
    or the download silently truncated."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_stable(spec_ids):
    """The tidy panel schema is identical across every indicator; drift here
    means the upstream sheet layout changed."""
    expected = {"ccode", "country", "year", "value"}
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert cols == expected, f"{sid}: columns {cols} != {expected}"


def test_years_plausible(spec_ids):
    """Clio Infra covers roughly 1500-2020; a year outside [1400, 2030] means a
    parse error (e.g. a value column read as the year column)."""
    import pyarrow.compute as pc
    for sid in spec_ids:
        years = load_raw_parquet(sid).column("year")
        lo, hi = pc.min(years).as_py(), pc.max(years).as_py()
        assert lo is not None and 1400 <= lo <= 2030, f"{sid}: min year {lo} implausible"
        assert hi is not None and 1400 <= hi <= 2030, f"{sid}: max year {hi} implausible"
