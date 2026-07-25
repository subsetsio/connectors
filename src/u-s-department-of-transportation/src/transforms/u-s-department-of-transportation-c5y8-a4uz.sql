-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "docket_number",
    CAST("usdot_number" AS BIGINT) AS usdot_number,
    "ins_form_code",
    CAST("ins_type_code" AS BIGINT) AS ins_type_code,
    "ins_class_code",
    CAST("max_cov_amount" AS DOUBLE) AS max_cov_amount,
    CAST("underl_lim_amount" AS DOUBLE) AS underl_lim_amount,
    "policy_no",
    strptime("effective_date", '%Y%m%d')::DATE AS effective_date,
    "insurance_company_name",
    strptime("trans_date", '%Y%m%d')::DATE AS trans_date
FROM "u-s-department-of-transportation-c5y8-a4uz"
