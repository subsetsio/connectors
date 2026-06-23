"""Health-invariant tests for GeyserTimes raw assets.

Run post-DAG inside the connector, reading raw through subsets_utils loaders so
they behave identically locally and in the cloud.
"""

from subsets_utils import load_raw_parquet, list_raw_files


def test_geysers_nonempty():
    """The geyser reference catalog must hold rows; empty means /geysers
    switched format or returned an error envelope."""
    table = load_raw_parquet("geysertimes-geysers")
    assert len(table) > 0, "geysertimes-geysers raw parquet has 0 rows"


def test_eruptions_batches_present_and_nonempty():
    """Eruptions are written one parquet batch per year. We expect many years
    of batches and a substantial total row count; a tiny total means year
    chunking silently dropped data."""
    files = list_raw_files("geysertimes-eruptions-*.parquet")
    assert len(files) >= 40, f"only {len(files)} eruption year-batches; expected >=40 (1970-present)"
    total = 0
    for f in files:
        asset_id = f.rsplit("/", 1)[-1][: -len(".parquet")]
        total += len(load_raw_parquet(asset_id))
    assert total >= 500000, f"only {total} eruption rows across all batches; expected >=500k"
