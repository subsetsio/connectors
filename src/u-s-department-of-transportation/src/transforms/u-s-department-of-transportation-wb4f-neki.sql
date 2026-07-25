-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "docket_number",
    CAST("usdot_number" AS BIGINT) AS usdot_number,
    "op_auth_type",
    strptime("order1_serve_date", '%Y%m%d')::DATE AS order1_serve_date,
    "order1_type_desc",
    strptime("order1_effective_date", '%Y%m%d')::DATE AS order1_effective_date
FROM "u-s-department-of-transportation-wb4f-neki"
