-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "UNIT" AS unit,
    "SEX" AS sex,
    "AGE" AS age,
    "MARSTA" AS marsta,
    "GEO" AS geo,
    CAST("TIME" AS BIGINT) AS time,
    "VALUES" AS values
FROM "ksh-a899cbc1-5223-4310-bd49-e31154f8bdb7"
