-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Northern Ireland electricity consumption rows are extracted cells; keep sheet, row_label, and series context when comparing geography or sector values.
SELECT
    "resource",
    CAST("sheet" AS BIGINT) AS sheet,
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-6e7e309e-d2b5-400d-92b7-dd520712aee7"
