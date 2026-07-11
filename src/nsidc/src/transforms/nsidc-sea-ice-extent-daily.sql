-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The early part of the daily series is not strictly daily; consumers should treat date as the observation date rather than assuming an uninterrupted daily calendar.
SELECT
    "hemisphere",
    "date",
    "year",
    "month",
    "day",
    "extent_million_sq_km",
    "missing_million_sq_km"
FROM "nsidc-sea-ice-extent-daily"
