-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "ntd_id",
    "agency_name",
    "city",
    "state",
    "organization_type",
    "reporter_type",
    CAST("agency_voms" AS BIGINT) AS agency_voms,
    "mode_name",
    "mode",
    "tos",
    CAST("mode_voms" AS BIGINT) AS mode_voms,
    "uace_code",
    "uza_name",
    CAST("primary_uza_population" AS BIGINT) AS primary_uza_population,
    "weblink",
    "weblink_justification",
    CAST("waived" AS BOOLEAN) AS waived,
    CAST("certification_flag" AS BOOLEAN) AS certification_flag,
    CAST("new_date_validated" AS TIMESTAMP) AS new_date_validated,
    CAST("new_modified_date" AS TIMESTAMP) AS new_modified_date
FROM "u-s-department-of-transportation-2u7n-ub22"
