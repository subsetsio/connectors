-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "self_managing_and_self_servicing",
    "age_group",
    "sex",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-th95.px"
