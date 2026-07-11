-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FREQ" AS freq,
    "UNIT" AS unit,
    "AGE" AS age,
    "GEO" AS geo,
    CAST("TIME" AS BIGINT) AS time,
    "VALUES" AS values
FROM "ksh-94904cf5-1b76-4c24-9375-65e743668f63"
