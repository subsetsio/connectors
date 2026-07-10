-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Solar PV cost data includes multiple capacity and cost breakdowns; retain row_label and series context before comparing values.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-738a7bdb-a533-443d-bd02-69a8dd7fe68d"
