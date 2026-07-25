-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "docket_number",
    "dot_number",
    CAST("sub_number" AS BIGINT) AS sub_number,
    "mod_col_1",
    "original_action_desc",
    strptime("orig_served_date", '%m/%d/%Y')::DATE AS orig_served_date,
    "disp_action_desc",
    strptime("disp_decided_date", '%m/%d/%Y')::DATE AS disp_decided_date,
    strptime("disp_served_date", '%m/%d/%Y')::DATE AS disp_served_date
FROM "u-s-department-of-transportation-9mw4-x3tu"
