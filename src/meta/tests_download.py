"""Post-DAG health invariants for the Meta connector (download stage).

Run in-connector after the DAG completes. `spec_ids` is the list of node ids
that ran (downloads + transforms). We verify full entity coverage and that
every raw asset actually materialized non-empty — a silent download/parse
regression (auth flip, format change, pagination break) trips these.
"""

EXPECTED_DOWNLOADS = {
    "meta-climate-change-opinion-survey",
    "meta-commuting-zones",
    "meta-cross-gender-ties",
    "meta-facebook-business-activity-trends-during-covid19",
    "meta-facebook-business-activity-trends-during-crisis",
    "meta-future-of-business-survey-aggregated-data",
    "meta-international-migration-flows",
    "meta-long-ties-data",
    "meta-movement-distribution",
    "meta-movement-range-maps",
    "meta-relative-wealth-index",
    "meta-social-capital-atlas",
    "meta-social-connectedness-index",
    "meta-social-connections-survey",
    "meta-survey-on-gender-equality-at-home",
    "meta-uk-social-capital-atlas",
}


def test_all_downloads_present(spec_ids):
    got = {i for i in spec_ids if not i.endswith("-transform")}
    missing = EXPECTED_DOWNLOADS - got
    assert not missing, f"missing download nodes: {sorted(missing)}"


def test_raw_assets_nonempty(spec_ids):
    from subsets_utils import load_raw_parquet

    downloads = [i for i in spec_ids if not i.endswith("-transform")]
    problems = []
    for asset in sorted(downloads):
        try:
            tbl = load_raw_parquet(asset)
        except Exception as e:  # noqa: BLE001 — surface the asset + error
            problems.append(f"{asset}: load failed ({type(e).__name__}: {e})")
            continue
        if tbl.num_rows == 0:
            problems.append(f"{asset}: 0 rows")
    assert not problems, f"raw asset problems: {problems}"
