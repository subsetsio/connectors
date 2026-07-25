-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "incident_id",
    "n_tmc",
    "direction",
    "road_inc",
    "road_tmc",
    CAST("start_time" AS TIMESTAMP) AS start_time,
    CAST("end_time" AS TIMESTAMP) AS end_time,
    "description",
    "weather"
FROM "u-s-department-of-transportation-r6ib-3rca"
