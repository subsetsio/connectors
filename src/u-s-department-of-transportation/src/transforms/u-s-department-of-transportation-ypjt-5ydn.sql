-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "prefix_docket_number",
    CAST("ins_type_code" AS BIGINT) AS ins_type_code,
    "ins_class_code",
    "max_cov_amount",
    "underl_lim_amount",
    "policy_no",
    strptime("effective_date", '%m/%d/%Y')::DATE AS effective_date,
    "ins_form_code",
    "name_company"
FROM "u-s-department-of-transportation-ypjt-5ydn"
