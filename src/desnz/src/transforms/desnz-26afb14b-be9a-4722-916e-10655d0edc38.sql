-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are extracted spreadsheet cells from multiple resources and sheets; use resource, sheet, row_label, and series together before aggregating values.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-26afb14b-be9a-4722-916e-10655d0edc38"
