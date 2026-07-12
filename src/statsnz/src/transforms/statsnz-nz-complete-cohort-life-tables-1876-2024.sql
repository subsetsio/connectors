-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("yearofbirth" AS BIGINT) AS yearofbirth,
    "sex",
    CAST("age" AS BIGINT) AS age,
    "percentile",
    CAST("dx" AS BIGINT) AS dx,
    CAST("ex" AS DOUBLE) AS ex,
    CAST("llx" AS BIGINT) AS llx,
    CAST("lx" AS BIGINT) AS lx,
    CAST("mx" AS DOUBLE) AS mx,
    CAST("px" AS DOUBLE) AS px,
    CAST("qx" AS DOUBLE) AS qx,
    CAST("sx" AS DOUBLE) AS sx
FROM "statsnz-nz-complete-cohort-life-tables-1876-2024"
