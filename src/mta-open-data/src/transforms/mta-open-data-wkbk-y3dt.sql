-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "service_date",
    "train",
    "branch",
    "depart_station",
    "depart_time",
    "arrive_station",
    "arrive_time",
    "period",
    "status",
    "minutes_late"
FROM "mta-open-data-wkbk-y3dt"
