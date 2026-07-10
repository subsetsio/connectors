-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: LSOA, MSOA, and IGZ estimates contain mixed geography levels and electricity/gas measures; filter geography level and fuel before aggregation.
SELECT
    "resource",
    CAST("sheet" AS BIGINT) AS sheet,
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-ed629618-7b69-465d-8e0a-0546b1809fc7"
