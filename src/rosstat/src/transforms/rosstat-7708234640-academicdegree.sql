-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("col_0" AS BIGINT) AS dimension_0,
    "col_1" AS dimension_1,
    "col_2" AS dimension_2
FROM "rosstat-7708234640-academicdegree"
