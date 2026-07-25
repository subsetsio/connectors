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
    "ins_cancl_form",
    "mod_col_2",
    "mod_col_3",
    "policy_no",
    CAST("min_cov_amount" AS BIGINT) AS min_cov_amount,
    "ins_class_code",
    strptime("effective_date", '%m/%d/%Y')::DATE AS effective_date,
    CAST("mod_col_4" AS BIGINT) AS mod_col_4,
    CAST("mod_col_5" AS BIGINT) AS mod_col_5,
    strptime("cancl_effective_date", '%m/%d/%Y')::DATE AS cancl_effective_date,
    "cancl_method",
    "inser_branch",
    "name_company"
FROM "u-s-department-of-transportation-6sqe-dvqs"
