-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "docket_number",
    "dot_number",
    "ins_form_code",
    "mod_col_1",
    "name_company",
    "policy_no",
    strptime("trans_date", '%m/%d/%Y')::DATE AS trans_date,
    CAST("underl_lim_amount" AS BIGINT) AS underl_lim_amount,
    CAST("max_cov_amount" AS BIGINT) AS max_cov_amount,
    strptime("effective_date", '%m/%d/%Y')::DATE AS effective_date,
    strptime("cancl_effective_date", '%m/%d/%Y')::DATE AS cancl_effective_date
FROM "u-s-department-of-transportation-qh9u-swkp"
