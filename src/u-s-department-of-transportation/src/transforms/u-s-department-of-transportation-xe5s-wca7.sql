-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "docket_number",
    CAST("usdot_number" AS BIGINT) AS usdot_number,
    "ins_form_code",
    "filing_status_reason",
    CAST("ins_type_code" AS BIGINT) AS ins_type_code,
    "ins_type_ind",
    "policy_no",
    "ins_type_desc",
    CAST("min_cov_amount" AS DOUBLE) AS min_cov_amount,
    "ins_class_code",
    strptime("effective_date", '%Y%m%d')::DATE AS effective_date,
    CAST("underl_lim_amount" AS DOUBLE) AS underl_lim_amount,
    CAST("max_cov_amount" AS DOUBLE) AS max_cov_amount,
    strptime("cancl_effective_date", '%Y%m%d')::DATE AS cancl_effective_date,
    "insurance_company_name"
FROM "u-s-department-of-transportation-xe5s-wca7"
