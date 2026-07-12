-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex_of_foetus",
    "cause_of_death_by_icd_10",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-rv66.px"
