-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Census 2021 CMD tables include category totals alongside detailed categories; filter category dimensions before summing across rows.
SELECT
    "lower_tier_local_authorities_code",
    "lower_tier_local_authorities",
    CAST("sex_2_categories_code" AS BIGINT) AS sex_2_categories_code,
    "sex_2_categories",
    CAST("age_91_categories_code" AS BIGINT) AS age_91_categories_code,
    "age_91_categories",
    "value"
FROM "ons-ts009"
