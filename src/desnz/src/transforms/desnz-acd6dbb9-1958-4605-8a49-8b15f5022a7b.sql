-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Green Homes Grant LAD and HUG data contains multiple schemes, measures, and household breakdowns; filter programme and measure context before aggregation.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-acd6dbb9-1958-4605-8a49-8b15f5022a7b"
