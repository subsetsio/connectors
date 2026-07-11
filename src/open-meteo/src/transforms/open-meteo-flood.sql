-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: River discharge is sampled at the connector's curated locations and only rows with a source-reported discharge value are published.
SELECT
    "name",
    "country",
    "latitude",
    "longitude",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "river_discharge"
FROM "open-meteo-flood"
