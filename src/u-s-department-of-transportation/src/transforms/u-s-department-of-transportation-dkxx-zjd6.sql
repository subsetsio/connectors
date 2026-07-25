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
    "mode",
    "mode_name",
    "type_of_service",
    CAST("mode_voms" AS BIGINT) AS mode_voms,
    CAST("vehicle_operations" AS BIGINT) AS vehicle_operations,
    "vehicle_operations_1",
    CAST("vehicle_maintenance" AS BIGINT) AS vehicle_maintenance,
    "vehicle_maintenance_1",
    CAST("facility_maintenance" AS BIGINT) AS facility_maintenance,
    "facility_maintenance_1",
    CAST("general_administration" AS BIGINT) AS general_administration,
    "general_administration_1",
    CAST("reduced_reporter_expenses" AS BIGINT) AS reduced_reporter_expenses,
    "reduced_reporter_expenses_1",
    CAST("total" AS BIGINT) AS total,
    "total_questionable",
    CAST("separate_report_amount" AS BIGINT) AS separate_report_amount,
    "separate_report_amount_1"
FROM "u-s-department-of-transportation-dkxx-zjd6"
