-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("dot_number" AS BIGINT) AS dot_number,
    "legal_name",
    "dba_name",
    strptime("oos_date", '%Y-%m-%d')::DATE AS oos_date,
    "oos_reason",
    "status",
    strptime("rescind_date", '%Y-%m-%d')::DATE AS rescind_date
FROM "u-s-department-of-transportation-p2mt-9ige"
