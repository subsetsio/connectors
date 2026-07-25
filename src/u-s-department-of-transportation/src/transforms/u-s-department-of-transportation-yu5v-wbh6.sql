-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "docket_number",
    CAST("usdot_number" AS BIGINT) AS usdot_number,
    "op_auth_type",
    "op_auth_status",
    "reason",
    strptime("status_change_date", '%Y%m%d')::DATE AS status_change_date
FROM "u-s-department-of-transportation-yu5v-wbh6"
