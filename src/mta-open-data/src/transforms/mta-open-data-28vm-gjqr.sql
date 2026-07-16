-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "year",
    "month",
    "day_of_week",
    "hour_of_day",
    "timestamp",
    "origin_station_complex_id",
    "origin_station_complex_name",
    "origin_latitude",
    "origin_longitude",
    "destination_station_complex_id",
    "destination_station_complex_name",
    "destination_latitude",
    "destination_longitude",
    "estimated_average_ridership",
    "origin_point",
    "destination_point"
FROM "mta-open-data-28vm-gjqr"
