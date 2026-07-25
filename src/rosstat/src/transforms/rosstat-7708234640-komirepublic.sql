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
    "col_4",
    "col_5",
    "col_6",
    "col_7",
    "col_8",
    "col_9",
    "col_10",
    "col_11",
    "col_12",
    "col_13",
    "col_14",
    "col_15"
FROM "rosstat-7708234640-komirepublic"
