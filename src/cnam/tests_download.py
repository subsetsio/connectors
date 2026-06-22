"""Post-DAG health invariants for the CNAM connector.

These run in-connector after the DAG, loading raw through the same
`subsets_utils` parquet loader the download node used. They catch silent
degradation that file-existence alone misses: an empty/truncated export, or a
format switch that drops the shared `annee` time dimension every CNAM series has.
"""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every bulk export should return rows. An empty parquet means the ODS
    export endpoint changed format, errored softly, or returned a stub."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_all_have_year_dimension(spec_ids):
    """Every CNAM dataset is an annual/periodic series keyed by `annee`. A
    missing year column means the export schema drifted and the published
    table would lose its time axis."""
    missing = [sid for sid in spec_ids if "annee" not in load_raw_parquet(sid).column_names]
    assert not missing, f"raw assets missing the 'annee' column: {missing}"
