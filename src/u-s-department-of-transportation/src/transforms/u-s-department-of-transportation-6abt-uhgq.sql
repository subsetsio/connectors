-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "agency",
    "city",
    "state",
    "ntd_id",
    "organization_type",
    "reporter_type",
    CAST("report_year" AS BIGINT) AS report_year,
    "uace_code",
    "uza_name",
    CAST("primary_uza_population" AS BIGINT) AS primary_uza_population,
    CAST("agency_voms" AS BIGINT) AS agency_voms,
    "vehicle_type",
    CAST("_0" AS BIGINT) AS 0,
    CAST("_1" AS BIGINT) AS 1,
    CAST("_2" AS BIGINT) AS 2,
    CAST("_3" AS BIGINT) AS 3,
    CAST("_4" AS BIGINT) AS 4,
    CAST("_5" AS BIGINT) AS 5,
    CAST("_6" AS BIGINT) AS 6,
    CAST("_7" AS BIGINT) AS 7,
    CAST("_8" AS BIGINT) AS 8,
    CAST("_9" AS BIGINT) AS 9,
    CAST("_10" AS BIGINT) AS 10,
    CAST("_11" AS BIGINT) AS 11,
    CAST("_12" AS BIGINT) AS 12,
    CAST("_13_15" AS BIGINT) AS 13_15,
    CAST("_16_20" AS BIGINT) AS 16_20,
    CAST("_21_25" AS BIGINT) AS 21_25,
    CAST("_26_30" AS BIGINT) AS 26_30,
    CAST("_31_60" AS BIGINT) AS 31_60,
    CAST("_60" AS BIGINT) AS 60,
    CAST("total_vehicles" AS BIGINT) AS total_vehicles,
    CAST("average_age_of_fleet_in_years" AS BIGINT) AS average_age_of_fleet_in_years,
    CAST("average_lifetime_miles_per" AS BIGINT) AS average_lifetime_miles_per
FROM "u-s-department-of-transportation-6abt-uhgq"
