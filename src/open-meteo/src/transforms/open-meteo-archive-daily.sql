-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: ERA5 archive values are sampled only at the connector's curated locations, not every Open-Meteo coordinate.
SELECT
    "name",
    "country",
    "latitude",
    "longitude",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "precipitation_sum"
FROM "open-meteo-archive-daily"
