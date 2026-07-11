-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Occupational projection rows are indexed by area, projection period, and SOC; total openings should not be summed across overlapping occupational rollups.
SELECT
    "area",
    "period",
    "soc",
    "occupationtitle",
    CAST("baseyear" AS BIGINT) AS baseyear,
    CAST("projyear" AS BIGINT) AS projyear,
    CAST("change" AS BIGINT) AS change,
    CAST("percent" AS DOUBLE) AS percent,
    CAST("aopent" AS BIGINT) AS aopent,
    CAST("aopeng" AS BIGINT) AS aopeng,
    CAST("aopenr" AS BIGINT) AS aopenr
FROM "new-york-state-department-of-labor-pqm4-9qqb"
