-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "base_number",
    "wave_number",
    "base_name",
    "dba",
    "_years" AS years,
    "week_number",
    "pickup_start_date",
    "pickup_end_date",
    "total_dispatched_trips",
    "unique_dispatched_vehicle"
FROM "nyc-open-data-2bmr-jdsv"
