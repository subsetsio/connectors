-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "fiscal_year",
    "agency_code",
    "agency_name",
    "expensefunding",
    "category_name",
    "expense_or_funding_class_name",
    "expense_or_funding_code",
    "expense_or_funding_name",
    "current_year_adopt_amount",
    "current_year_current_modified_amount",
    "next_fiscal_year_amount"
FROM "nyc-open-data-iw4r-p85g"
