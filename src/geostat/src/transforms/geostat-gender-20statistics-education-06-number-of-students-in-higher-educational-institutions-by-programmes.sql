-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    "degree",
    "year",
    "programme",
    "higher_educational_institutions",
    "value"
FROM "geostat-gender-20statistics-education-06-number-of-students-in-higher-educational-institutions-by-programmes"
