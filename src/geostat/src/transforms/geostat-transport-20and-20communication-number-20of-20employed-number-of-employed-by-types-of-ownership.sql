-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ownership_type",
    "period",
    "value"
FROM "geostat-transport-20and-20communication-number-20of-20employed-number-of-employed-by-types-of-ownership"
