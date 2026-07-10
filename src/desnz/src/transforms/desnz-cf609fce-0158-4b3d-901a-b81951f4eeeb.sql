-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Residual fuel consumption includes multiple residual fuel types and geography levels; filter fuel and geography context before aggregation.
SELECT
    CAST("resource" AS BIGINT) AS resource,
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-cf609fce-0158-4b3d-901a-b81951f4eeeb"
