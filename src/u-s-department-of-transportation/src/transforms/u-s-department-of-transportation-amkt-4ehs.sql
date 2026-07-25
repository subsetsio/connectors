-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
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
    "mode",
    "mode_name",
    "type_of_service",
    CAST("mode_voms" AS BIGINT) AS mode_voms,
    CAST("major_mechanical_failures" AS BIGINT) AS major_mechanical_failures,
    "major_mechanical_failures_1",
    CAST("other_mechanical_failures" AS BIGINT) AS other_mechanical_failures,
    "other_mechanical_failures_1",
    CAST("total_mechanical_failures" AS BIGINT) AS total_mechanical_failures,
    "total_mechanical_failures_1",
    CAST("vehicle_passenger_car_miles" AS BIGINT) AS vehicle_passenger_car_miles,
    "vehicle_passenger_car_miles_1",
    CAST("vehicle_passenger_car_revenue" AS BIGINT) AS vehicle_passenger_car_revenue,
    "vehicle_passenger_car_miles_2",
    CAST("train_miles" AS BIGINT) AS train_miles,
    "train_miles_questionable",
    CAST("train_revenue_miles" AS BIGINT) AS train_revenue_miles,
    "train_revenue_miles_1"
FROM "u-s-department-of-transportation-amkt-4ehs"
