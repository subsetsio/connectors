-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "population_groups",
    CAST("by_years" AS BIGINT) AS by_years,
    "infectious_diseases",
    "value"
FROM "geostat-social-20statistics-health-morbidity-by-some-infectious"
