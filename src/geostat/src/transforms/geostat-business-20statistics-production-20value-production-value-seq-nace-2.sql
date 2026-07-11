-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kind_of_economic_activity",
    "period",
    "value"
FROM "geostat-business-20statistics-production-20value-production-value-seq-nace-2"
