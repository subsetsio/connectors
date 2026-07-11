-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "VARIABLE" AS variable,
    "BREAKDOWN" AS breakdown,
    "UNIT" AS unit,
    CAST("OBS_VALUE" AS BIGINT) AS obs_value,
    "FLAG" AS flag,
    "COMMENTS" AS comments
FROM "ksh-73a2a529-8e1c-4a8b-95a0-7c60c94b1b17"
