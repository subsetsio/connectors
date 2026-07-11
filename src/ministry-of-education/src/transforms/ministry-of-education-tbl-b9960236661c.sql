-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows preserve individual cells from Ministry of Education statistical grids; row and column labels can include totals or subtotals alongside component categories, so filter labels before aggregating values.
SELECT
    "entity_id",
    "year",
    "tbl_idx",
    "row_idx",
    "col_idx",
    "row_label",
    "col_label",
    "value"
FROM "ministry-of-education-tbl-b9960236661c"
