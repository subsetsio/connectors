-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a long-form extraction of monthly prefecture/region crosstabs; sheets, row labels, and column headers mix ports or regions with totals, subtotals, monthly values, annual cumulative values, and year-on-year comparisons, so filter to the intended measure before aggregating values.
SELECT
    "year",
    "classification",
    "sheet",
    "row_label",
    "col_header",
    "row_idx",
    "col_idx",
    "value"
FROM "kobe-customs-kenbetsu"
