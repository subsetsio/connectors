"""Health invariants for the raw football-data.co.uk assets.

These run post-DAG inside the connector and read raw via the same loader the
fetch fns wrote with, catching silent degradation (empty/truncated payloads,
discovery that broke and pulled only a handful of files).
"""

from subsets_utils import load_raw_parquet


def test_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_main_corpus_substantial(spec_ids):
    """~690 (season, division) files of a few hundred matches each => well
    over 100k rows. A small count means discovery silently truncated."""
    sid = "football-data-co-uk-matches-main"
    if sid in spec_ids:
        n = len(load_raw_parquet(sid))
        assert n >= 100_000, f"{sid}: only {n} rows; expected >=100k"


def test_extra_corpus_substantial(spec_ids):
    """16 country files, each stacking many seasons => tens of thousands."""
    sid = "football-data-co-uk-matches-extra"
    if sid in spec_ids:
        n = len(load_raw_parquet(sid))
        assert n >= 20_000, f"{sid}: only {n} rows; expected >=20k"


def test_main_has_recent_season(spec_ids):
    """The current/most-recent season must be present, else the live files
    stopped being discovered."""
    sid = "football-data-co-uk-matches-main"
    if sid in spec_ids:
        seasons = set(load_raw_parquet(sid).column("Season").to_pylist())
        assert len(seasons) >= 25, f"{sid}: only {len(seasons)} distinct seasons"
