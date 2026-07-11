-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "positions",
    "years",
    "type_of_institutions",
    "value"
FROM "geostat-social-20statistics-education-higher-number-of-professors-in-higher-education"
