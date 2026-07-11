-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "AGE" AS age,
    "C_BIRTH" AS c_birth,
    "UNIT" AS unit,
    "SEX" AS sex,
    "GEO" AS geo,
    CAST("TIME" AS BIGINT) AS time,
    "VALUES" AS values
FROM "ksh-1604a8a4-aea7-4f86-866b-63b1980f77eb"
