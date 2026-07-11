-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "CITIZEN" AS citizen,
    "AGE" AS age,
    "UNIT" AS unit,
    "SEX" AS sex,
    "GEO" AS geo,
    CAST("TIME" AS BIGINT) AS time,
    "VALUES" AS values
FROM "ksh-5c5c1828-8599-4b96-8b9f-ef6c27ab7c82"
