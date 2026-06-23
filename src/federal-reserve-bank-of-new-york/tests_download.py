"""Health-invariant tests for the NY Fed Markets connector.

Run post-DAG inside the connector; loads raw assets via subsets_utils loaders.
Catches silent degradation (empty payloads, wrong format) that file existence
alone misses.
"""

from subsets_utils import load_raw_ndjson, load_raw_parquet

# Which loader each download spec wrote with.
NDJSON_SPECS = {
    "federal-reserve-bank-of-new-york-reference-rates",
    "federal-reserve-bank-of-new-york-treasury-operations",
    "federal-reserve-bank-of-new-york-agency-mbs-operations",
    "federal-reserve-bank-of-new-york-repo-operations",
    "federal-reserve-bank-of-new-york-securities-lending-operations",
    "federal-reserve-bank-of-new-york-central-bank-fx-swaps",
    "federal-reserve-bank-of-new-york-primary-dealer-series",
    "federal-reserve-bank-of-new-york-primary-dealer-market-share",
    "federal-reserve-bank-of-new-york-soma-summary",
}
PARQUET_SPECS = {
    "federal-reserve-bank-of-new-york-primary-dealer-values",
    "federal-reserve-bank-of-new-york-soma-holdings",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw asset should hold rows. Empty payloads usually mean the
    endpoint switched format or the response envelope changed silently."""
    for sid in spec_ids:
        if sid in PARQUET_SPECS:
            n = len(load_raw_parquet(sid))
        else:
            n = len(load_raw_ndjson(sid))
        assert n > 0, f"{sid}: raw asset has 0 rows"


def test_pd_values_large(spec_ids):
    """The primary-dealer bulk CSV is the largest asset (~740k rows); a small
    count means the CSV download truncated or only a header came back."""
    sid = "federal-reserve-bank-of-new-york-primary-dealer-values"
    if sid in spec_ids:
        n = len(load_raw_parquet(sid))
        assert n >= 300000, f"{sid}: only {n} rows; bulk CSV likely truncated"
