-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Commercial pipeline rows are forward-looking procurement plans and may be revised or withdrawn; do not treat entries as committed spend.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-b6a31316-c69b-44c6-babd-d0b76448b030"
