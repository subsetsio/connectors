-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "UNIT" AS unit,
    "GEO" AS geo,
    CAST("TIME" AS BIGINT) AS time,
    "VALUES" AS values
FROM "ksh-99ac9e47-dc1b-44d8-8e69-cd88018c0244"
