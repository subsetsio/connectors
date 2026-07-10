-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Provisional greenhouse-gas emissions are subject to later revision and include multiple accounting bases; filter measure and sector context before comparison.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-9a1e58e5-d1b6-457d-a414-335ca546d52c"
