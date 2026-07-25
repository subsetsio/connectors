-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("cntrl_sec_id" AS DOUBLE) AS cntrl_sec_id,
    "category",
    "participant",
    CAST("timestamp" AS DOUBLE) AS timestamp,
    CAST("speed_mph" AS DOUBLE) AS speed_mph,
    CAST("lat" AS DOUBLE) AS lat,
    CAST("long" AS DOUBLE) AS long,
    "category_group",
    CAST("ride_date" AS TIMESTAMP) AS ride_date,
    CAST("age" AS DOUBLE) AS age,
    "sex",
    "bike_type",
    "e_bike_class",
    "bike_experience_roundup",
    "bike_experience_binary",
    CAST("demoyes" AS BIGINT) AS demoyes,
    "location",
    CAST("experience_on_trail" AS BOOLEAN) AS experience_on_trail
FROM "u-s-department-of-transportation-kyh2-psz2"
