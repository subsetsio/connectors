-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("col_0" AS BIGINT) AS dimension_0,
    CAST("col_1" AS BIGINT) AS dimension_1,
    "col_2" AS dimension_2,
    "col_3" AS dimension_3
FROM "rosstat-7708234640-okei"
