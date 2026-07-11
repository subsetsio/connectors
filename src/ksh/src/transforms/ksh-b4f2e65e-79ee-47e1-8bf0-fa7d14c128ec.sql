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
FROM "ksh-b4f2e65e-79ee-47e1-8bf0-fa7d14c128ec"
