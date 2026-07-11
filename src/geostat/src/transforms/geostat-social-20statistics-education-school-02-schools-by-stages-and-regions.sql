-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type",
    "year",
    "region",
    "value"
FROM "geostat-social-20statistics-education-school-02-schools-by-stages-and-regions"
