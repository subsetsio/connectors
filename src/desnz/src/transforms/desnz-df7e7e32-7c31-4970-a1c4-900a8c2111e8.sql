-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The current downloaded Prompt Payment Data raw profile is empty, so publication may require a download repair or explicit waiver.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-df7e7e32-7c31-4970-a1c4-900a8c2111e8"
