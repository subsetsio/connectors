-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Road transport consumption includes geography, vehicle type, and fuel breakdowns; filter the relevant level before aggregation.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-995df3b9-993e-403b-a527-a62ff0b56ca3"
