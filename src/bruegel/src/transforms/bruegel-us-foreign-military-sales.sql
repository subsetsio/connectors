-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: One row per announced US foreign military sale, keyed by the source's own id. These are announcements, not deliveries or settled contracts: financial_value_bn_usd is the announced ceiling value, and a sale announced in one year may never be executed. Year and month date the announcement.
SELECT
    "id",
    "country",
    "financial_value",
    "main_equipment",
    "additional_equipment",
    "quantities",
    "military_domain",
    "general_item_type",
    "specific_item_type",
    "contractors",
    "year",
    "month",
    "2024_deflator_value",
    "financial_value_2024_prices",
    "EU_non-EU" AS eu_non_eu,
    "NATO_non-NATO" AS nato_non_nato,
    "region"
FROM "bruegel-us-foreign-military-sales"
