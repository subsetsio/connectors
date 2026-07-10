-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The file is a headerless historical alert corpus and contains repeated alert records; use it as a source log rather than a deduplicated incident table.
SELECT
    "col_1",
    "col_2",
    "col_3",
    "col_4",
    "col_5",
    CAST("col_6" AS BIGINT) AS col_6,
    "col_7",
    "col_8",
    "col_9",
    "col_10",
    CAST("col_11" AS BIGINT) AS col_11,
    CAST("col_12" AS BIGINT) AS col_12,
    CAST("col_13" AS BIGINT) AS col_13,
    CAST("col_14" AS BIGINT) AS col_14,
    "col_15",
    CAST("col_16" AS DOUBLE) AS col_16,
    CAST("col_17" AS DOUBLE) AS col_17
FROM "global-health-h1n1-healthmap-2009-2012"
