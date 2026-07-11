-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_of_educational_institution",
    CAST("years" AS BIGINT) AS years,
    "regions_educational_institution_form",
    "value"
FROM "geostat-social-20statistics-education-professional-number-of-institu"
