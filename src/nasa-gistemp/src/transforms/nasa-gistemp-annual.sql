-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Values are temperature anomalies in degrees Celsius relative to the 1951-1980 baseline; they should not be interpreted as absolute temperatures.
-- caution: The region column contains Global, Northern Hemisphere, and Southern Hemisphere series; filter to the intended region before trend analysis.
SELECT
    "year",
    "region",
    "anomaly_c"
FROM "nasa-gistemp-annual"
