-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    "child_s_birth_weight_grams",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-rv19.px"
