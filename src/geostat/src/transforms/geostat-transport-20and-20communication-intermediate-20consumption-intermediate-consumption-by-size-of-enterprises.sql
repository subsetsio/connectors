-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "enterprise_size",
    CAST("petriod" AS BIGINT) AS petriod,
    "value"
FROM "geostat-transport-20and-20communication-intermediate-20consumption-intermediate-consumption-by-size-of-enterprises"
