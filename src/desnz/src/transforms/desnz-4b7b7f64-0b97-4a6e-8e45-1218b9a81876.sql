-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Sub-national final energy consumption includes mixed fuels, sectors, and geography levels; filter the relevant dimensions before summing.
SELECT
    CAST("resource" AS BIGINT) AS resource,
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-4b7b7f64-0b97-4a6e-8e45-1218b9a81876"
