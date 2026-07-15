-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "year",
    "industry1",
    "industry2",
    "industry3",
    "at_least_one",
    "parttime_work",
    "flexihours",
    "staggered_time",
    "teleworking",
    "homeworking",
    "job_sharing",
    "compressed_work_schedule"
FROM "sg-data-d-43079cc099f6ac0315db856e570103ce"
