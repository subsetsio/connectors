-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Heat pump deployment data includes capacity, geography, technology, and period breakdowns; filter to one basis before aggregating.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-b264edb9-4a78-4977-a871-c9561a3ef8cc"
