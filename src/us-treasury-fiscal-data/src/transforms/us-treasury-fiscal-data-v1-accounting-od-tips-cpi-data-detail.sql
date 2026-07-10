-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cusip",
    "original_issue_date",
    "index_date",
    CAST(NULLIF("ref_cpi", 'null') AS DOUBLE) AS ref_cpi,
    CAST(NULLIF("index_ratio", 'null') AS DOUBLE) AS index_ratio,
    "pdf_link",
    "xml_link"
FROM "us-treasury-fiscal-data-v1-accounting-od-tips-cpi-data-detail"
