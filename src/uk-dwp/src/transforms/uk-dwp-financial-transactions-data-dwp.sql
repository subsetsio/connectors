-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are unioned from monthly spend CSV resources whose supplier, amount, date, and identifier columns changed names over time; choose the relevant period-specific columns before summing spend.
-- caution: Use `resource_name` and `resource_last_modified` to identify the source period or file before aggregating.
SELECT
    "resource_name",
    "resource_id",
    CAST("resource_last_modified" AS TIMESTAMP) AS resource_last_modified,
    "source_url",
    "row_index",
    CAST("account_code" AS BIGINT) AS account_code,
    "amount",
    "cleansed_supplier",
    "col_8",
    CAST("cost_centre" AS BIGINT) AS cost_centre,
    "date",
    "department",
    "departmental_family",
    "entity",
    "expenditure_area",
    "expenditure_type",
    "expense_area",
    "expense_area_1",
    "expense_type",
    "identifier",
    "indentifier",
    "invoice_account_description",
    "invoice_cost_centre_description",
    "invoice_distribution_amount",
    "invoice_number",
    "invoice_paid_date",
    "payment_number",
    "sop_supplier_name",
    "supplier",
    "supplier_name",
    "transaction_number",
    "transparency_invoice_amount",
    "unique_id",
    "unique_identifier"
FROM "uk-dwp-financial-transactions-data-dwp"
