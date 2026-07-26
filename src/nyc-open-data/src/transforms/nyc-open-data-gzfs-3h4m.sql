-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "agency_code",
    "agency_name",
    "budget_function",
    "budget_function_description",
    "row_id",
    "spending_type",
    "spending_type_description",
    "first_actual_fiscal_year",
    "year_1_actual",
    "year_2_actual",
    "year_3_actual",
    "first_plan_fiscal_year",
    "plan_amount_year_1",
    "plan_amount_year_2"
FROM "nyc-open-data-gzfs-3h4m"
