-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "state_ntd_id",
    "ntd_id",
    "agency_name",
    "agency_status",
    CAST("last_active_report_year" AS BIGINT) AS last_active_report_year,
    "reporter_type",
    "reporting_module",
    "city",
    "state",
    "census_year",
    "primary_uza_name",
    "uace_code",
    CAST("uza_area_sq_miles" AS DOUBLE) AS uza_area_sq_miles,
    CAST("uza_population" AS BIGINT) AS uza_population,
    "field",
    CAST("report_year" AS BIGINT) AS report_year,
    CAST("value" AS BIGINT) AS value
FROM "u-s-department-of-transportation-ectq-t3k3"
