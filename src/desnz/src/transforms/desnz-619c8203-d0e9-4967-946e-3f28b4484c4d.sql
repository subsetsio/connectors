-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Off-gas-network estimates include multiple geography and property breakdowns; filter row_label and series context before aggregation.
SELECT
    "resource",
    CAST("sheet" AS BIGINT) AS sheet,
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-619c8203-d0e9-4967-946e-3f28b4484c4d"
