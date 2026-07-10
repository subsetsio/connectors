-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Special adviser transparency returns contain meetings, gifts, and hospitality records in related sheets; filter activity type before counting.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-5370c0bb-d3bb-4a45-829a-1437018fe13d"
