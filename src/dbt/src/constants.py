"""Fetch parameters for the DBT Data API connector.

Data, not logic: maps each download spec id (one per rank-accepted collect
entity) to the (dataset, kind, source_id) triple needed to build its
data-endpoint URL. The node module imports this and stays logic-only.

spec id == f"dbt-{entity_id.lower().replace('_', '-')}" for the entity union
at data/sources/dbt/work/entity_union.json.
"""

# spec_id -> (dataset_id, kind, source_id)   kind in {"table", "report"}
FETCH_PARAMS = {
    "dbt-market-barriers--barriers": (
        "market-barriers", "table", "barriers"),
    "dbt-orp-regulations--uk-regulatory-documents": (
        "orp-regulations", "table", "uk-regulatory-documents"),
    "dbt-uk-tariff-2021-01-01--commodities": (
        "uk-tariff-2021-01-01", "table", "commodities"),
    "dbt-uk-tariff-2021-01-01--measures": (
        "uk-tariff-2021-01-01", "table", "measures"),
    "dbt-uk-tariff-2021-01-01--measures-as-defined": (
        "uk-tariff-2021-01-01", "table", "measures-as-defined"),
    "dbt-uk-tariff-2021-01-01--measures-on-declarable-commodities": (
        "uk-tariff-2021-01-01", "table", "measures-on-declarable-commodities"),
    # NOTE: the report `measures-on-declarable-commodities` was an exact
    # duplicate of the table above (same schema, same ~1.1M rows) so it is not
    # published — see rank rule "duplicate".
    "dbt-uk-trade-quotas--quotas": (
        "uk-trade-quotas", "table", "quotas"),
    "dbt-uk-trade-quotas--report--quotas-including-current-volumes": (
        "uk-trade-quotas", "report", "quotas-including-current-volumes"),
}
