-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are sub-basin observations; summing regions may not reproduce the hemisphere-wide extent series because the source publishes them as distinct products.
SELECT
    "hemisphere",
    "region",
    "date",
    "year",
    "month",
    "day",
    "area_sq_km",
    "extent_sq_km"
FROM "nsidc-sea-ice-regional-daily"
