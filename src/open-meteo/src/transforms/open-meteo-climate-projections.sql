-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are model-specific CMIP6 projections; filter or group by `model` before comparing or aggregating scenarios.
SELECT
    "name",
    "country",
    "latitude",
    "longitude",
    "model",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "temperature_2m_max"
FROM "open-meteo-climate-projections"
