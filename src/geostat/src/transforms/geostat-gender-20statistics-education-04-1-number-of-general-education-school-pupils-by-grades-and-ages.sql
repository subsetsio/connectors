-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "grades",
    "status",
    "year",
    "age",
    "gender",
    "value"
FROM "geostat-gender-20statistics-education-04-1-number-of-general-education-school-pupils-by-grades-and-ages"
