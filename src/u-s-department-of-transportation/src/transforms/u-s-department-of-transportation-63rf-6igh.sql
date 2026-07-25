-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("report_year" AS BIGINT) AS report_year,
    "ntd_id",
    "reporter_name",
    "mode",
    "type_of_service",
    CAST("start_date" AS TIMESTAMP) AS start_date,
    CAST("end_date" AS TIMESTAMP) AS end_date,
    "reporting_period",
    CAST("monthid" AS BIGINT) AS monthid,
    CAST("year" AS BIGINT) AS year,
    CAST("month_year" AS BIGINT) AS month_year,
    CAST("incident_created_date" AS TIMESTAMP) AS incident_created_date,
    CAST("incidentupdated_date" AS TIMESTAMP) AS incidentupdated_date,
    CAST("submission_date" AS TIMESTAMP) AS submission_date,
    "safety_security_indicator",
    "event_type",
    "location",
    "transit_worker_assault",
    "location_type",
    "additional_assault_information",
    CAST("event_count" AS BIGINT) AS event_count,
    CAST("customer_injuries" AS BIGINT) AS customer_injuries,
    CAST("worker_injuries" AS BIGINT) AS worker_injuries,
    CAST("other_injuries" AS BIGINT) AS other_injuries,
    CAST("total_non_major_injuries" AS BIGINT) AS total_non_major_injuries,
    CAST("non_major_physical_assaults" AS BIGINT) AS non_major_physical_assaults,
    CAST("non_major_non_physical" AS BIGINT) AS non_major_non_physical,
    CAST("non_major_physical_assaults_1" AS BIGINT) AS non_major_physical_assaults_1,
    CAST("non_major_non_physical_1" AS BIGINT) AS non_major_non_physical_1
FROM "u-s-department-of-transportation-63rf-6igh"
