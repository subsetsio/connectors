-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Northern Ireland gas consumption rows are extracted cells; retain sheet, row_label, and series context when comparing domestic and non-domestic values.
SELECT
    "resource",
    CAST("sheet" AS BIGINT) AS sheet,
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-86a4555e-6f38-4529-8647-542cc6223162"
