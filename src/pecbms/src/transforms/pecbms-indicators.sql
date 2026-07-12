-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix European, EU, regional, and habitat indicator groups; filter by indicator_group or region before comparing or aggregating indicator results.
SELECT
    "indicator_id",
    "indicator_name",
    "indicator_group",
    "region",
    "time_period",
    "species_count",
    "trend_percent"
FROM "pecbms-indicators"
