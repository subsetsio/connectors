-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "C_BIRTH" AS c_birth,
    "AGE" AS age,
    "UNIT" AS unit,
    "SEX" AS sex,
    "GEO" AS geo,
    CAST("TIME" AS BIGINT) AS time,
    "VALUES" AS values
FROM "ksh-33b9d9ea-4fc0-4d9e-a96e-23459adb470b"
