-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "schedule_day_type",
    "time_period",
    "line",
    "direction",
    "stop_path_id",
    "average_actual_runtime",
    "_25th_percentile_runtime" AS "25th_percentile_runtime",
    "_50th_percentile_runtime" AS "50th_percentile_runtime",
    "_75th_percentile_runtime" AS "75th_percentile_runtime",
    "actual_trains",
    "distance",
    "average_speed",
    "average_scheduled_runtime",
    "scheduled_trains",
    "origin_station_id",
    "destination_station_id",
    "origin_station_name",
    "destination_station_name",
    "number_of_stops"
FROM "mta-open-data-sp9g-mzjh"
