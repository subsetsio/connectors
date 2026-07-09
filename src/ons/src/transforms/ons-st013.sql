-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Census 2021 CMD tables include category totals alongside detailed categories; filter category dimensions before summing across rows.
SELECT
    "regions_code",
    "regions",
    CAST("age_86_categories_code" AS BIGINT) AS age_86_categories_code,
    "age_86_categories",
    CAST("sex_2_categories_code" AS BIGINT) AS sex_2_categories_code,
    "sex_2_categories",
    "value"
FROM "ons-st013"
