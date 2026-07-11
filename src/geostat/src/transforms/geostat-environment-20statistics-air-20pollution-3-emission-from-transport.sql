-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "hazardous_substances",
    "value"
FROM "geostat-environment-20statistics-air-20pollution-3-emission-from-transport"
