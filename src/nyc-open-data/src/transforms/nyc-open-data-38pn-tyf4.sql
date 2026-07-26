-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "_year" AS year,
    "_quarter" AS quarter,
    "reimbursement_amount"
FROM "nyc-open-data-38pn-tyf4"
