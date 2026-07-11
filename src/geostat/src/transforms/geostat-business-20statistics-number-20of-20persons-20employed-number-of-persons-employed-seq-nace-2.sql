-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kind_of_economic_activity",
    "period",
    "value"
FROM "geostat-business-20statistics-number-20of-20persons-20employed-number-of-persons-employed-seq-nace-2"
