-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Operational forecast rows are forward-looking and ephemeral; each refresh replaces the current forecast horizon rather than extending a stable history.
SELECT
    "name",
    "country",
    "latitude",
    "longitude",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum"
FROM "open-meteo-forecast"
