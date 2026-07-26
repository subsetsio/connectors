-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "col_0" AS dimension_0,
    "col_1" AS dimension_1,
    "col_2" AS dimension_2,
    "col_3" AS dimension_3,
    "col_4" AS dimension_4,
    "col_5" AS dimension_5,
    "col_6" AS dimension_6,
    "col_7" AS dimension_7,
    "col_8" AS dimension_8,
    "col_9" AS dimension_9,
    "col_10" AS dimension_10,
    "col_11" AS dimension_11
FROM "rosstat-7708234640-ptor"
