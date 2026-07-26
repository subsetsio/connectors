-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_month" AS month,
    "school_district",
    "average_ride_time_minutes",
    "month_1",
    "school_district_1",
    "average_ride_time_minutes_1",
    "month_2",
    "school_district_2",
    "average_ride_time_minutes_2"
FROM "nyc-open-data-s6qk-qkvb"
