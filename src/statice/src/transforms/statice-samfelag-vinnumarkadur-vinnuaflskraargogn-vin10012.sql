-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_table_id" AS table_id,
    "_table_name" AS table_name,
    "_source_updated" AS source_updated,
    "obs_value",
    "obs_time",
    "month",
    "region",
    "sex",
    "age_groups",
    "origin"
FROM "statice-samfelag-vinnumarkadur-vinnuaflskraargogn-vin10012"
