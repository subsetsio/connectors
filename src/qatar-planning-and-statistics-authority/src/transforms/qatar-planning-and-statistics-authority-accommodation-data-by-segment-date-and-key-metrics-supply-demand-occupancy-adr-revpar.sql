-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "segment",
    strptime("date", '%Y-%m')::DATE AS date,
    "supply",
    "demand",
    "occupancy_rate",
    "average_daily_rate",
    "revenue_per_available_room",
    "sample_properties",
    "sample_rooms",
    "census_properties",
    "census_rooms"
FROM "qatar-planning-and-statistics-authority-accommodation-data-by-segment-date-and-key-metrics-supply-demand-occupancy-adr-revpar"
