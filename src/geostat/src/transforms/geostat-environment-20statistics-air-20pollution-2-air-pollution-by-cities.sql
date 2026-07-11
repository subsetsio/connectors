-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "hazardous_substances",
    CAST("year" AS BIGINT) AS year,
    "city",
    "value"
FROM "geostat-environment-20statistics-air-20pollution-2-air-pollution-by-cities"
