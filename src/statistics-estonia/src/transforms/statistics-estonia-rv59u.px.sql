-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "marital_status",
    "sex",
    "age_group",
    "county",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-rv59u.px"
