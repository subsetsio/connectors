-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Historical electricity tables include multiple fuels, generation, supply, and consumption measures; keep row_label and series context before aggregating.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-93c3228c-0ad6-4e87-98c2-6a2b965d53b7"
