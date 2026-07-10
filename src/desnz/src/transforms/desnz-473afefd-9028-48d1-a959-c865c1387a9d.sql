-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: NEED data contains mixed building, geography, and consumption breakdowns; filter resource, sheet, and series before comparison or aggregation.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-473afefd-9028-48d1-a959-c865c1387a9d"
