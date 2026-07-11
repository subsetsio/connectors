-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is the connector's curated sampling frame, not a complete Open-Meteo location catalog.
SELECT
    "name",
    "country",
    "latitude",
    "longitude"
FROM "open-meteo-locations"
