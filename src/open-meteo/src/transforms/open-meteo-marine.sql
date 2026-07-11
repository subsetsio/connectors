-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Marine wave rows are forecast-only and ephemeral; each refresh replaces the current forecast horizon rather than extending a stable history.
SELECT
    "name",
    "country",
    "latitude",
    "longitude",
    CAST("time" AS TIMESTAMP) AS time,
    "wave_height",
    "wave_period",
    "wave_direction"
FROM "open-meteo-marine"
