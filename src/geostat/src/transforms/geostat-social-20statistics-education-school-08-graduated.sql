-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    CAST("years" AS BIGINT) AS years,
    "institution",
    "value"
FROM "geostat-social-20statistics-education-school-08-graduated"
