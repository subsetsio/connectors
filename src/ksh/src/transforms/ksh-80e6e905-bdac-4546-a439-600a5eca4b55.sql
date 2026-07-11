-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "VARIABLE" AS variable,
    "BREAKDOWN" AS breakdown,
    "UNIT" AS unit,
    CAST("OBS_VALUE" AS BIGINT) AS obs_value
FROM "ksh-80e6e905-bdac-4546-a439-600a5eca4b55"
