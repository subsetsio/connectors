-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "department",
    "_month" AS month,
    "fiscal_year",
    "current_month_actual",
    "yeartodate_actual",
    "fiscal_year_plan",
    "fund"
FROM "nyc-open-data-4xfc-mzbg"
