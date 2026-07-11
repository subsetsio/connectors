-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    "year",
    "region",
    "value"
FROM "geostat-gender-20statistics-education-07-number-of-students-at-the-higher-educational-institutions-as-to-beginning-of-academic-year"
