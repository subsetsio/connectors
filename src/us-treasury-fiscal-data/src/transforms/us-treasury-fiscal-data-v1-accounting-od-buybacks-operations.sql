-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "operation_date",
    "operation_start_time_est",
    "operation_close_time_est",
    "settlement_date",
    "preliminary_ann_pdf",
    "preliminary_ann_xml",
    "final_ann_pdf",
    "final_ann_xml",
    "results_pdf",
    "results_xml",
    "special_ann_pdf",
    "operation_type",
    "security_type",
    "maturity_bucket",
    "nbr_issues_accepted",
    CAST(NULLIF("total_par_amt_offered", 'null') AS DOUBLE) AS total_par_amt_offered,
    CAST(NULLIF("par_amt_per_offer", 'null') AS DOUBLE) AS par_amt_per_offer,
    "max_par_amt_redeemed",
    "max_nbr_offers",
    CAST(NULLIF("nbr_issues_eligible", 'null') AS BIGINT) AS nbr_issues_eligible,
    "total_par_amt_accepted"
FROM "us-treasury-fiscal-data-v1-accounting-od-buybacks-operations"
