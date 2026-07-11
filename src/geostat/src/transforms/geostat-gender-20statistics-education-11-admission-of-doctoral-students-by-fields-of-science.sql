-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    CAST("years" AS BIGINT) AS years,
    "fields_of_science",
    "value"
FROM "geostat-gender-20statistics-education-11-admission-of-doctoral-students-by-fields-of-science"
