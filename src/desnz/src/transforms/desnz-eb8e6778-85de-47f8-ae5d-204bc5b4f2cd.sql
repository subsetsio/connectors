-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Sub-national gas consumption includes geography levels and domestic/non-domestic breakdowns; filter geography and consumer group before aggregation.
SELECT
    "resource",
    CAST("sheet" AS BIGINT) AS sheet,
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-eb8e6778-85de-47f8-ae5d-204bc5b4f2cd"
