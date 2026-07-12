-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are daily quantile-style activity measures by GADM geography and business vertical; do not sum activity_quantile across geographies or verticals.
SELECT
    "gadm_id",
    "gadm_name",
    "gadm_level",
    "gadm0_name",
    "gadm1_name",
    "gadm2_name",
    "country",
    "business_vertical",
    "activity_quantile",
    "activity_percentage",
    "crisis_ds",
    "ds",
    "_source_file" AS source_file
FROM "meta-facebook-business-activity-trends-during-covid19"
