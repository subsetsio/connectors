-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "VARIABLE" AS variable,
    "BREAKDOWN" AS breakdown,
    "UNIT" AS unit,
    CAST("OBS_VALUE" AS BIGINT) AS obs_value
FROM "ksh-2da67fcb-ff5d-4549-a66d-433d37bec6d1"
