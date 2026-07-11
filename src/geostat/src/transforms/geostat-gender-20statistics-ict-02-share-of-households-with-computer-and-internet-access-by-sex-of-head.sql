-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type",
    "year",
    "sex",
    "value"
FROM "geostat-gender-20statistics-ict-02-share-of-households-with-computer-and-internet-access-by-sex-of-head"
