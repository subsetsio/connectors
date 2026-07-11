-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    "degree",
    "year",
    "program",
    "institutions",
    "value"
FROM "geostat-gender-20statistics-education-08-graduates-of-higher-educational-institutions-by-programs-in-2011-2014"
