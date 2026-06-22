"""Health invariants run post-DAG, in-connector, through subsets_utils loaders.
Catch silent degradation that file-existence alone misses: a truncated repo
file, a parser that emitted near-zero rows, a column quietly going all-null.
"""

from subsets_utils import load_raw_parquet


def test_downloads_has_history(spec_ids):
    if "bioconductor-downloads" not in spec_ids:
        return
    table = load_raw_parquet("bioconductor-downloads")
    assert len(table) > 100000, f"downloads raw has only {len(table)} rows"
    repos = set(table.column("repo").to_pylist())
    assert repos == {"bioc", "data-experiment", "data-annotation", "workflows"}, (
        f"downloads missing repos: got {sorted(repos)}"
    )


def test_packages_catalog_complete(spec_ids):
    if "bioconductor-packages" not in spec_ids:
        return
    table = load_raw_parquet("bioconductor-packages")
    assert len(table) > 3000, f"packages raw has only {len(table)} rows"
    # title should be populated for the vast majority of packages
    titles = table.column("title").to_pylist()
    non_null = sum(1 for t in titles if t)
    assert non_null > 0.8 * len(titles), (
        f"only {non_null}/{len(titles)} packages have a title; DCF parse likely degraded"
    )
