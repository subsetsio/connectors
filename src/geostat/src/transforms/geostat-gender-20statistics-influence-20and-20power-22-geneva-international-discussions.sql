-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    "year",
    "value"
FROM "geostat-gender-20statistics-influence-20and-20power-22-geneva-international-discussions"
