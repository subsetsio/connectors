-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are unioned from separate CSV resources with financial-year and period columns that vary by file; filter to the intended period representation before comparing percentages.
SELECT
    "resource_name",
    "resource_id",
    CAST("resource_last_modified" AS TIMESTAMP) AS resource_last_modified,
    "source_url",
    "row_index",
    "financial_year_2015_to_2016",
    "financial_year_2016_to_2017",
    "financial_year_2017_to_2018",
    "financial_year_2018_to_2019",
    "financial_year_2019_to_2020",
    "financial_year_2020_to_2021",
    "late_payment_interest",
    "percentage_of_invoices_paid_within_30_days",
    "percentage_of_invoices_paid_within_5_days",
    "period"
FROM "uk-dwp-dwp-prompt-payment-data"
