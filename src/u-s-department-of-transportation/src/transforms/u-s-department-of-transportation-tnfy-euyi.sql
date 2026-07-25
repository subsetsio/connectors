-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "ntd_id",
    "reporter_name",
    "uza_name",
    "uace_code",
    "mode",
    "type_of_service",
    "data_point",
    CAST("begin_date" AS TIMESTAMP) AS begin_date,
    CAST("end_date" AS TIMESTAMP) AS end_date,
    CAST("percentage_change" AS DOUBLE) AS percentage_change,
    CAST("value" AS BIGINT) AS value,
    "reported_by"
FROM "u-s-department-of-transportation-tnfy-euyi"
