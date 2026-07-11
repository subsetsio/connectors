-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    "years",
    "region",
    "value"
FROM "geostat-gender-20statistics-education-10-number-of-students-enrolled-at-the-higher-educational-institutions-by-regions-as-to-beginning-of-academic-year"
