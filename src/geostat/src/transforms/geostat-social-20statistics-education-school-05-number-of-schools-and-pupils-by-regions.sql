-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "years",
    "indicators",
    "municipalities",
    "value"
FROM "geostat-social-20statistics-education-school-05-number-of-schools-and-pupils-by-regions"
