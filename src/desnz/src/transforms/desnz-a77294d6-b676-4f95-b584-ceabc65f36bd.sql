-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Social Housing Decarbonisation Fund data contains programme delivery breakdowns across resources and sheets; filter measure and geography context before aggregating.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-a77294d6-b676-4f95-b584-ceabc65f36bd"
