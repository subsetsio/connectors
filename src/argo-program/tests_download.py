"""Health-invariant tests for the Argo Program raw metadata assets."""

from subsets_utils import load_raw_parquet


def test_metadata_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: metadata parquet has 0 rows"


def test_metadata_contains_variables(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        row_types = table.column("row_type").to_pylist()
        variables = table.column("variable_name").to_pylist()
        assert "variable" in row_types, f"{sid}: no variable rows"
        assert any(v for v in variables), f"{sid}: no variable names"


def test_metadata_source_urls_are_erddap(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        urls = set(table.column("source_url").to_pylist())
        assert len(urls) == 1, f"{sid}: expected one metadata source URL"
        url = next(iter(urls))
        assert url.startswith("https://erddap.ifremer.fr/erddap/info/"), url
