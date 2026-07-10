-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: RHI and RHPP data contains multiple scheme, technology, geography, and status breakdowns; filter the relevant sheet and series before summing.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-28d823ff-310b-4620-8ba2-58dbd1d0c7c5"
