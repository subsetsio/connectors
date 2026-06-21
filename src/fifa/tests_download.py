"""Health invariants for the FIFA World Ranking raw downloads."""

import pyarrow.parquet as pq
from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {
    "release_date", "gender", "rank", "id_team", "team_name",
    "country_code", "total_points", "previous_rank", "previous_points",
    "confederation",
}


def _check(asset: str, gender: str) -> None:
    table = load_raw_parquet(asset)
    assert set(table.column_names) == EXPECTED_COLUMNS, set(table.column_names)
    assert table.num_rows > 5000, table.num_rows
    genders = set(table.column("gender").to_pylist())
    assert genders == {gender}, genders
    ranks = [r for r in table.column("rank").to_pylist() if r is not None]
    assert min(ranks) == 1, min(ranks)
    dates = set(table.column("release_date").to_pylist())
    assert len(dates) > 50, len(dates)


def test_men_world_ranking():
    _check("fifa-men-world-ranking", "men")


def test_women_world_ranking():
    _check("fifa-women-world-ranking", "women")
