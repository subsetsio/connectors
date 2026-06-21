"""Post-DAG health invariants for the HM Land Registry connector.

These run in-connector via subsets_utils loaders, so they behave identically
locally and on GitHub Actions. They target silent degradation that file
existence alone misses: a truncated bulk host, a region API that switched
format, or a flattening that dropped the measures.
"""

from subsets_utils import list_raw_files, load_raw_ndjson, load_raw_parquet


def test_ppd_year_batches_present():
    """PPD is written one parquet batch per year (~30 years since 1995). A
    handful means the bulk host changed scheme or stopped redirecting."""
    files = list_raw_files("hm-land-registry-ppd-*")
    assert len(files) >= 25, f"only {len(files)} PPD year batches: {files[:5]}"


def test_ppd_batch_nonempty():
    """At least one PPD year batch must carry rows and the 16-column schema."""
    files = sorted(list_raw_files("hm-land-registry-ppd-*"))
    assert files, "no PPD batches at all"
    # Strip directory + .parquet to recover the asset id for the loader.
    asset = files[-1].split("/")[-1].rsplit(".", 1)[0]
    table = load_raw_parquet(asset)
    assert table.num_rows > 0, f"{asset}: 0 rows"
    assert "price" in table.column_names and "transaction_id" in table.column_names


def test_ukhpi_nonempty():
    """UKHPI spans ~405 regions x hundreds of months — tens of thousands of
    rows. A small count means region enumeration or pagination broke."""
    rows = load_raw_ndjson("hm-land-registry-ukhpi")
    assert len(rows) >= 50000, f"ukhpi has only {len(rows)} rows"
    sample = rows[0]
    assert sample.get("region_slug"), "ukhpi row missing region_slug"
    assert sample.get("ref_month"), "ukhpi row missing ref_month"
    assert "averagePrice" in sample, "ukhpi row missing the averagePrice measure"


def test_ukhpi_region_coverage():
    """Distinct regions in the published raw should match the ~405 enumerated."""
    rows = load_raw_ndjson("hm-land-registry-ukhpi")
    regions = {r["region_slug"] for r in rows}
    assert len(regions) >= 300, f"only {len(regions)} distinct UKHPI regions"
