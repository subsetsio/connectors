-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("yearmonth", '%Y-%m')::DATE AS yearmonth,
    "license_class",
    "trips_per_day",
    "farebox_per_day",
    "unique_drivers",
    "unique_vehicles",
    "vehicles_per_day",
    "avg_days_vehicles_on_road",
    "avg_hours_per_day_per_vehicle",
    "avg_days_drivers_on_road",
    "avg_hours_per_day_per_driver",
    "avg_minutes_per_trip",
    "percent_of_trips_paid_with_credit_card",
    "trips_per_day_shared"
FROM "nyc-open-data-v6kb-cqej"
