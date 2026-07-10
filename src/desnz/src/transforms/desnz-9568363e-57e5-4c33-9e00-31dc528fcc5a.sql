-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Final greenhouse-gas emissions include different gases, source sectors, end-user views, and industrial classifications; filter the accounting basis before summing.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-9568363e-57e5-4c33-9e00-31dc528fcc5a"
