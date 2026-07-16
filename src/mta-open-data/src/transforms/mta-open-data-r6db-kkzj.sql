-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "day_type",
    "hour_of_day",
    "time_period",
    "route_type",
    "route_id",
    "cbd_relation",
    "sum_mileage",
    "sum_time",
    "average_road_speed"
FROM "mta-open-data-r6db-kkzj"
