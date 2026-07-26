-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "plan",
    "revenues_in_thousands",
    "salaries_in_thousands",
    "communication_expenses_in_thousands",
    "advisory_and_auditing_fees_in_thousands",
    "rent_reimbursement_to_the_city_for_overhead_in_thousands",
    "administrative_support_in_thousands",
    "recordkeeping_loan_fees_in_thousands",
    "custodian_fees_in_thousands",
    "total_expenses_in_thousands"
FROM "nyc-open-data-w65z-zif5"
