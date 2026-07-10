-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "digits",
    "section",
    "division",
    "group",
    "class",
    "item",
    "desc_en",
    "exclude_en",
    "include_en",
    "desc_bm",
    "exclude_bm",
    "include_bm"
FROM "dosm-msic"
