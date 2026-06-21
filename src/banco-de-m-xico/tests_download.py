"""Health invariants for the Banco de México download.

These run post-DAG against the raw parquet written by the `values` download node,
through the same subsets_utils loader. They catch silent degradation that a bare
file-exists check misses: empty payloads, missing columns, all-null observations,
or a date column that stopped being DD/MM/YYYY.
"""
from subsets_utils import load_raw_parquet


def test_raw_nonempty(spec_ids):
    """Every download spec's raw asset must hold rows. Empty usually means the
    endpoint changed or the token expired silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_columns(spec_ids):
    """Raw must carry the six string columns the transform reads."""
    expected = {"series_id", "title", "unit", "frequency", "fecha", "dato"}
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = expected - cols
        assert not missing, f"{sid}: missing columns {missing}"


def test_multiple_series_present(spec_ids):
    """The curated corpus spans many series; a collapse to one id signals the
    batched request silently dropped ids."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        n_series = len(set(table.column("series_id").to_pylist()))
        assert n_series >= 5, f"{sid}: only {n_series} distinct series in raw"


def test_observations_parseable(spec_ids):
    """At least some observations must look like real DD/MM/YYYY dates with
    numeric values — guards against an all-'N/E' or reformatted payload."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        fechas = table.column("fecha").to_pylist()
        datos = table.column("dato").to_pylist()
        good = sum(
            1
            for f, d in zip(fechas, datos)
            if f and len(f) == 10 and f[2] == "/" and f[5] == "/"
            and d and d != "N/E"
        )
        assert good > 0, f"{sid}: no parseable date/value observations"
