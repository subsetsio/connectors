-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Road-fuel sales, delivery, and stock rows include different measures and reporting bases; filter to a single measure before comparing over time.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-9003012e-4564-4a6b-b5f0-8765ccb23a03"
