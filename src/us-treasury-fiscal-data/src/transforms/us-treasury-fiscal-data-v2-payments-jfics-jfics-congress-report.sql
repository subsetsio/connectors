-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "judgment_type_cd",
    "defendant_agency_nm",
    "submitting_agency_nm",
    CAST(NULLIF("control_nbr", 'null') AS BIGINT) AS control_nbr,
    "plaintiffs_counsel_nm",
    "payment_id",
    "payment_sent_dt",
    "confirmed_payment_amt",
    "principal_amt",
    "principal_citation_cd",
    "principal_citation_desc",
    "attorneys_fee_amt",
    "attorneys_fee_citation_cd",
    "attorneys_fee_citation_desc",
    "cost_amt",
    "cost_citation_cd",
    "cost_citation_desc",
    "interest_amt",
    "interest_citation_cd",
    "interest_citation_desc",
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr
FROM "us-treasury-fiscal-data-v2-payments-jfics-jfics-congress-report"
