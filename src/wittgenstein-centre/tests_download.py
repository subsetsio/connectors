"""Health-invariant tests run post-DAG, in-connector, against the raw assets.

Catch silent degradation that file-existence alone misses: truncated downloads,
a scenario file silently dropped from the projection union, or the recode
dictionary losing its region map (which would break code decoding downstream).
"""

from subsets_utils import load_raw_parquet

_SCENARIOS = {"SSP1", "SSP2", "SSP2mig0", "SSP2mig2x", "SSP3", "SSP4", "SSP5"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download asset must hold rows; an empty payload usually means the
    Zenodo endpoint changed format or the transfer truncated."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_projection_union_has_all_scenarios(spec_ids):
    """The detailed projection asset unions 7 per-scenario files; if one file
    went missing the union silently loses a scenario."""
    sid = "wittgenstein-centre-projection-results"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    got = set(table.column("scenario").to_pylist())
    assert got == _SCENARIOS, f"{sid}: scenarios {got} != expected {_SCENARIOS}"
    # ~1.2M rows per scenario file observed during probing.
    assert table.num_rows > 6_000_000, f"{sid}: only {table.num_rows} rows — a file truncated?"


def test_recode_has_region_and_edu_maps(spec_ids):
    """The recode dictionary decodes region/education codes in every other
    transform; losing those rows would null out names downstream."""
    sid = "wittgenstein-centre-recode-dictionary"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    vars_present = set(table.column("var").to_pylist())
    assert "region" in vars_present, "recode dictionary missing region map"
    assert "edu" in vars_present, "recode dictionary missing edu map"
