-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("calendar_year" AS BIGINT) AS calendar_year,
    CAST("week" AS BIGINT) AS week,
    CAST("_change_all_vehicles" AS BIGINT) AS change_all_vehicles,
    CAST("_change_passenger" AS BIGINT) AS change_passenger,
    CAST("_change_truck" AS BIGINT) AS change_truck
FROM "u-s-department-of-transportation-yeig-3uz6"
