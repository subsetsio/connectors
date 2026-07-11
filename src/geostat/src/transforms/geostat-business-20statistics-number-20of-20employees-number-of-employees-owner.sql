-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ownership_types",
    "period",
    "value"
FROM "geostat-business-20statistics-number-20of-20employees-number-of-employees-owner"
