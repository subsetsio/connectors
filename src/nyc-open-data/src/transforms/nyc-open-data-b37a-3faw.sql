-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "published_date",
    "project_type",
    "project_type_description",
    "tenyear_plan_category",
    "funding_type",
    "first_fiscal_year",
    "fiscal_year_1_amount",
    "fiscal_year_2_amount",
    "fiscal_year_3_amount",
    "fiscal_year_4_amount",
    "fiscal_year_5_amount",
    "fiscal_year_6_amount",
    "fiscal_year_7_amount",
    "fiscal_year_8_amount",
    "fiscal_year_9_amount",
    "fiscal_year_10_amount",
    "tenyear_total"
FROM "nyc-open-data-b37a-3faw"
