-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are a faithful long-form melt of one CBSL workbook; row_label and col_label encode the workbook stub/header text and may mix totals, subcategories, geographies, units, or period labels depending on the source table.
SELECT
    "row_label",
    "col_label",
    "period_year",
    "value",
    "value_text"
FROM "central-bank-of-sri-lanka-table-2.18"
