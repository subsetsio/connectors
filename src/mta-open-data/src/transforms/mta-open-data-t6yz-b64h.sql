-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "toll_date",
    "toll_hour",
    "toll_10_minute_block",
    "minute_of_hour",
    "hour_of_day",
    "day_of_week_int",
    "day_of_week",
    "toll_week",
    "time_period",
    "vehicle_class",
    "detection_group",
    "detection_region",
    "crz_entries",
    "excluded_roadway_entries"
FROM "mta-open-data-t6yz-b64h"
