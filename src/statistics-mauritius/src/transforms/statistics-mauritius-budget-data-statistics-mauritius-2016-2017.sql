-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Budget rows are administrative line items; totals and subtotals may appear with detailed lines, so filter by category and item level before aggregating amounts.
SELECT
    "Head" AS head,
    "ExpenseType" AS expensetype,
    CAST("ItemNo" AS BIGINT) AS itemno,
    "Category" AS category,
    "SubCategory" AS subcategory,
    CAST("StartFinancialYear" AS BIGINT) AS startfinancialyear,
    CAST("EndFinancialYear" AS BIGINT) AS endfinancialyear,
    "FinancialStatus" AS financialstatus,
    CAST("Amount" AS DOUBLE) AS amount,
    "__row_number" AS row_number,
    "__package_id" AS package_id,
    "__package_name" AS package_name,
    "__package_title" AS package_title,
    CAST("__package_metadata_modified" AS TIMESTAMP) AS package_metadata_modified,
    "__resource_id" AS resource_id,
    "__resource_name" AS resource_name,
    "__resource_format" AS resource_format,
    CAST("__resource_last_modified" AS TIMESTAMP) AS resource_last_modified
FROM "statistics-mauritius-budget-data-statistics-mauritius-2016-2017"
