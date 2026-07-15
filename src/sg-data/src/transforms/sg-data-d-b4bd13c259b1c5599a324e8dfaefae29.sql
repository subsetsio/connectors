-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "year",
    "at_least_one",
    "parttime_work",
    "flexihours",
    "staggered_time",
    "teleworking",
    "homeworking",
    "job_sharing",
    "compressed_work_schedule"
FROM "sg-data-d-b4bd13c259b1c5599a324e8dfaefae29"
