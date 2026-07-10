-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("claim_control_number" AS BIGINT) AS claim_control_number,
    "Part" AS part,
    "DRG" AS drg,
    "HCPCS Procedure Code" AS hcpcs_procedure_code,
    "Provider Type" AS provider_type,
    "Type of Bill" AS type_of_bill,
    "Review Decision" AS review_decision,
    "Error Code" AS error_code
FROM "cms-6395b458-2f89-4828-8c1a-e1e16b723d48"
