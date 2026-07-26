-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "case_type",
    "report_date",
    "caseload",
    "percentage",
    "amount"
FROM "nyc-open-data-g2dh-zf5t"
