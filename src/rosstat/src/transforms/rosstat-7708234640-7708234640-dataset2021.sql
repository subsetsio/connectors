-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw table; treat rows as source records rather than mergeable observations.
SELECT
    "col_0" AS dimension_0,
    "col_1" AS dimension_1,
    "col_2" AS dimension_2,
    "col_3" AS dimension_3,
    "col_4" AS dimension_4,
    "col_5" AS dimension_5,
    "col_6" AS dimension_6,
    "col_7" AS dimension_7
FROM "rosstat-7708234640-7708234640-dataset2021"
