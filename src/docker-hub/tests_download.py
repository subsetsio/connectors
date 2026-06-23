from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw asset should hold rows. An empty payload usually means
    the listing endpoint switched format or the namespace moved."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_official_images_count_sane(spec_ids):
    """The library namespace held ~179 official images; a gutted catalog (<100)
    means pagination stopped after page 1."""
    sid = "docker-hub-official-images"
    if sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 100, f"{sid}: only {len(table)} rows; expected ~179"


def test_pull_stats_have_positive_totals(spec_ids):
    """Pull counts for the most-used base images are large; an all-zero column
    means the API stopped populating the field."""
    sid = "docker-hub-pull-stats"
    if sid in spec_ids:
        table = load_raw_parquet(sid)
        pulls = table.column("pull_count").to_pylist()
        assert any((p or 0) > 0 for p in pulls), f"{sid}: no positive pull_count values"
