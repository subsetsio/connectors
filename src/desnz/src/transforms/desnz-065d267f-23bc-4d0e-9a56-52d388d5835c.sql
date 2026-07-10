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
FROM "desnz-065d267f-23bc-4d0e-9a56-52d388d5835c"
