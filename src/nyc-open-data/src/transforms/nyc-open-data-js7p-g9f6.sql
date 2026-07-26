-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "fiscal_year",
    "program_category",
    "program_area",
    "action_plan_allocation",
    "adjusted_city_spending",
    "federal_reimbursement"
FROM "nyc-open-data-js7p-g9f6"
