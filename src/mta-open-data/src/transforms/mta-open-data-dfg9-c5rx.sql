-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "fiscal_year",
    "month",
    "scenario",
    "financial_plan_year",
    "expense_type",
    "agency",
    "type",
    "subtype",
    "general_ledger",
    "account_category",
    "account_subcategory_1",
    "account_subcategory_2",
    "amount"
FROM "mta-open-data-dfg9-c5rx"
