-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    CAST("year" AS BIGINT) AS year,
    "causes_of_death",
    "value"
FROM "geostat-gender-20statistics-health-20care-11-mortality-by-causes-of-death"
