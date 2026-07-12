-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are unioned from many monthly CSV resources whose headers changed over time; equivalent concepts can appear in different columns across resource periods.
-- caution: Use `resource_name` and `resource_last_modified` to identify the source period or file before aggregating.
SELECT
    "resource_name",
    "resource_id",
    "resource_last_modified",
    "source_url",
    "row_index",
    "amount",
    "col_5",
    "col_6",
    "comment",
    "comments",
    "date",
    "description",
    "expense_description",
    "fin_expense_description",
    "fin_transaction_amount",
    "july_2022_gov_uk_title",
    CAST("line" AS BIGINT) AS line,
    CAST("line_no" AS BIGINT) AS line_no,
    "line_number",
    "mch_merchant_category_code_mcc",
    "mch_merchant_name",
    "merchant",
    "merchant_name",
    "posting_date",
    "reason",
    "supplier",
    "supplier_and_location",
    "supplier_name",
    "title_lang_en_dwp_and_cmg_spending_over_500",
    "transaction_amount",
    strptime("transaction_date", '%d/%m/%Y')::DATE AS transaction_date,
    CAST("transaction_ref_number" AS BIGINT) AS transaction_ref_number,
    CAST("transaction_reference_number" AS BIGINT) AS transaction_reference_number,
    strptime("transcation_posting_date", '%d/%m/%Y')::DATE AS transcation_posting_date
FROM "uk-dwp-dwp-government-procurement-card-payments-over-500"
