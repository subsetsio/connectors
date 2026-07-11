-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_and_quarter",
    "topic",
    "topic_subgroup",
    "indicator",
    "race_ethnicity_category",
    "rate",
    "unit",
    "significant"
FROM "nchs-76vv-a7x8"
