-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year and Quarter" AS year_and_quarter,
    "Topic" AS topic,
    "Topic Subgroup" AS topic_subgroup,
    "Indicator" AS indicator,
    "Race Ethnicity Category" AS race_ethnicity_category,
    CAST("Rate" AS DOUBLE) AS rate,
    "Unit" AS unit,
    "Significant" AS significant
FROM "cdc-76vv-a7x8"
