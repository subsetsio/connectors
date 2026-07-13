-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_table_id" AS table_id,
    "_table_name" AS table_name,
    "_source_updated" AS source_updated,
    "obs_value",
    CAST("obs_time" AS BIGINT) AS obs_time,
    CAST("year" AS BIGINT) AS year,
    "cultural_and_creative_industry",
    "unit"
FROM "statice-samfelag-menning-6-hagraenirmaelikvardar-2-starfandilaunasumma-men10201"
