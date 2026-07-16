-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "agency",
    "asset",
    "power_source",
    "total",
    "useful_life",
    "percent_beyond_useful_life",
    "planned_bus_purchases_2025_2029",
    "planned_bus_purchases_2030_2034",
    "planned_bus_purchases_2035_2039",
    "planned_bus_purchases_2040_2044"
FROM "mta-open-data-pssf-s7fa"
