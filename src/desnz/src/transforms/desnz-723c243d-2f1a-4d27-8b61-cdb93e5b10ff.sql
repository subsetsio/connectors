-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Local authority greenhouse-gas emissions include regional aggregates, sectors, and gases; filter geography and measure context before summing.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-723c243d-2f1a-4d27-8b61-cdb93e5b10ff"
