"""Health invariants for the DHS Program raw downloads.

These run post-DAG, in-connector, through subsets_utils loaders — so they catch
silent degradation (empty payloads, a country crawl that fetched nothing, an
endpoint that switched format) that file-existence alone would miss.
"""
from subsets_utils import list_raw_files, load_raw_ndjson


def test_data_batches_present_and_nonempty():
    """The /data crawl writes one NDJSON batch per country with data. DHS has
    92 countries; if far fewer batches landed, the per-country crawl broke."""
    files = list_raw_files("dhs-program-data-*")
    assert len(files) >= 80, f"expected ~92 country batches, got {len(files)}: {files[:5]}"


def test_data_records_have_values():
    """At least one country batch should hold rows carrying numeric Values."""
    files = list_raw_files("dhs-program-data-*")
    assert files, "no dhs-program-data batches found"
    # strip the .ndjson.zst extension to recover the asset id the loader wants
    asset = files[0].split(".")[0]
    rows = load_raw_ndjson(asset)
    assert len(rows) > 0, f"{asset}: batch has 0 records"
    assert any(r.get("Value") is not None for r in rows), f"{asset}: no rows carry a Value"
    assert all("DataId" in r and "IndicatorId" in r for r in rows[:50]), \
        f"{asset}: records missing expected fact keys"


def test_indicators_catalog_nonempty():
    rows = load_raw_ndjson("dhs-program-indicators")
    assert len(rows) > 1000, f"indicators catalog unexpectedly small: {len(rows)} rows"
    assert all("IndicatorId" in r for r in rows[:50]), "indicator records missing IndicatorId"


def test_surveys_catalog_nonempty():
    rows = load_raw_ndjson("dhs-program-surveys")
    assert len(rows) > 100, f"surveys catalog unexpectedly small: {len(rows)} rows"
    assert all("SurveyId" in r for r in rows[:50]), "survey records missing SurveyId"
