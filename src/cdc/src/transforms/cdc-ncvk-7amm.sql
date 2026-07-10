-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State" AS state,
    "Sex" AS sex,
    CAST("LEB" AS DOUBLE) AS leb,
    CAST("SE" AS DOUBLE) AS se,
    "Quartile" AS quartile
FROM "cdc-ncvk-7amm"
