-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The observation table contains monthly values by station; aggregate across months or stations only after choosing the weather measure and time window intentionally.
SELECT
    "station",
    "year",
    "month",
    "tmax_degc",
    "tmin_degc",
    "af_days",
    "rain_mm",
    "sun_hours",
    "provisional"
FROM "met-office-observations"
