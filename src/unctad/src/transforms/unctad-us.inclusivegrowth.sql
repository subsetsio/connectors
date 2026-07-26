-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "economy",
    "economy_label",
    "category",
    "category_label",
    "inclusive_growth",
    "inclusive_growth_footnote",
    "inclusive_growth_missing_value"
FROM "unctad-us.inclusivegrowth"
