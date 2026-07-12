-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "time_of_birth",
    "sex",
    "cause_of_death_by_icd_10",
    CAST("year_of_death" AS BIGINT) AS year_of_death,
    "value"
FROM "statistics-estonia-rv67.px"
