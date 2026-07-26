-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "published_date",
    "project_type",
    "project_type_name",
    "budget_line",
    "budget_line_title",
    "funding_type",
    "first_fiscal_year",
    "fiscal_year_1_amount",
    "fiscal_year_2_amount",
    "fiscal_year_3_amount",
    "fiscal_year_4_amount"
FROM "nyc-open-data-46m8-77gv"
