"""Health-invariant tests, run post-DAG inside the connector.

These catch silent degradation that file-existence alone misses: an endpoint
that starts returning an HTML error page (0 rows / wrong columns), a truncated
download, or a vintage bump that empties a file.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every CSP workbook has hundreds-to-thousands of rows; an empty parquet
    means the .xls came back as an error page or the file was retired."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_country_column_present(spec_ids):
    """Every CSP dataset is keyed on a country (column 'country', or for the
    terrorist-bombings event list the place column 'location'). A missing
    country/place column means the header row was misparsed."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert cols & {"country", "location"}, (
            f"{sid}: no country/location column; columns were {sorted(cols)}"
        )
