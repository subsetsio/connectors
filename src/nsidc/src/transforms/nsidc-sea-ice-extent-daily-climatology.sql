-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is a fixed 1981-2010 day-of-year climatology, not an observed time series; join to observations by day_of_year and hemisphere before computing anomalies.
SELECT
    "hemisphere",
    "day_of_year",
    "average_extent_million_sq_km",
    "std_deviation_million_sq_km",
    "pct_10",
    "pct_25",
    "pct_50",
    "pct_75",
    "pct_90"
FROM "nsidc-sea-ice-extent-daily-climatology"
