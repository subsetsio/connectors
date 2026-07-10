-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Senior-official transparency returns contain expenses, hospitality, and meetings in related sheets; filter activity type before counting records.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-d6da4831-de12-4a2b-958b-c0c0bfe61e05"
