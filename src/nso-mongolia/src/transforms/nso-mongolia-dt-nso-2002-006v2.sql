-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Indicator" AS indicator,
    CAST("Он" AS BIGINT) AS column,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-2002-006v2"
