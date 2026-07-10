-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Anonymised NEED datasets are extracted as cells from large files; use the source resource and sheet layout to interpret repeated labels.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-7390402c-e7ce-4e2f-bb08-d8d65f852f47"
