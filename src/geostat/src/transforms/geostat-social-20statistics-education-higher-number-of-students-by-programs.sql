-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "level_of_education",
    "years",
    "programmes",
    "type_of_institutions",
    "value"
FROM "geostat-social-20statistics-education-higher-number-of-students-by-programs"
