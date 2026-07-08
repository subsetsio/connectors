SELECT
    CAST("State_Territory" AS VARCHAR) AS state,
    2013 AS year,
    CAST("Total" AS BIGINT) AS total,
    CAST("R_worker" AS BIGINT) AS retirement_workers,
    CAST("R_spouse" AS BIGINT) AS retirement_spouses,
    CAST("R_child" AS BIGINT) AS retirement_children,
    CAST("S_widow_parent" AS BIGINT) AS survivors_widowers_parents,
    CAST("S_child" AS BIGINT) AS survivors_children,
    CAST("D_worker" AS BIGINT) AS disability_workers,
    CAST("D_spouse" AS BIGINT) AS disability_spouses,
    CAST("D_child" AS BIGINT) AS disability_children,
    CAST("Men65_older" AS BIGINT) AS men_65_older,
    CAST("Women65_older" AS BIGINT) AS women_65_older
FROM "ssa-oasdi--2013--1"
WHERE "State_Territory" IS NOT NULL AND TRIM(CAST("State_Territory" AS VARCHAR)) <> ''
