-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "beginning_accuracy",
    "beginning_cross_street",
    CAST("beginning_milepost" AS DOUBLE) AS beginning_milepost,
    "core_details",
    CAST("end_date" AS TIMESTAMP) AS end_date,
    "end_date_accuracy",
    "ending_accuracy",
    "ending_cross_street",
    CAST("ending_milepost" AS DOUBLE) AS ending_milepost,
    "lanes",
    "location_method",
    "multipoint",
    "restrictions",
    CAST("start_date" AS TIMESTAMP) AS start_date,
    "start_date_accuracy",
    "types_of_work",
    "vehicle_impact"
FROM "u-s-department-of-transportation-b55b-fde7"
