-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix reporting countries, border points, flow/trade types, products, units, and quantity/value measures; filter those dimensions before aggregating flows.
SELECT
    "reporting_country",
    "reporting_country_code",
    "border_point",
    "source",
    "source_country_code",
    "destination",
    "destination_country_code",
    "cpcv2",
    "product",
    "source_organization",
    "source_document",
    "collection_status",
    "period_date",
    "flow_type",
    "trade_type",
    "unit",
    "unit_type",
    "unit_name",
    "status",
    "value",
    "common_unit",
    "common_unit_quantity",
    "reporting_country_geographic_group",
    "reporting_country_fewsnet_region",
    "source_geographic_group",
    "source_fewsnet_region",
    "destination_geographic_group",
    "destination_fewsnet_region",
    "start_date",
    "id",
    "dataseries_name",
    "collection_schedule",
    "data_usage_policy"
FROM "fews-net-tradeflowquantityvalue"
