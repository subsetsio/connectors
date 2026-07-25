-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw table; treat rows as source records rather than mergeable observations.
SELECT
    "col_0",
    "col_1",
    "col_2",
    "col_3",
    CAST("col_4" AS BIGINT) AS col_4,
    "col_5",
    "col_6",
    "col_7",
    "col_8",
    CAST("col_9" AS BIGINT) AS col_9,
    "col_10",
    "col_11"
FROM "rosstat-7708234640-okato"
