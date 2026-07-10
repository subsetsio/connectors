-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Spending rows are extracted from monthly files and may include repeated supplier or transaction labels; retain resource and sheet context when comparing periods.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-1a7347c5-8758-427b-825b-31e0ff417784"
