-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Source spreadsheets are normalized to a long format; row_label, column, block, sheet, and row_dim carry table-specific dimensions and may include totals or subtotals, so filter the relevant labels before aggregating.
SELECT
    "sheet",
    "block",
    "row_dim",
    "row_label",
    "column",
    "col_index",
    "value",
    "value_num"
FROM "office-of-rail-and-road-table-1223"
