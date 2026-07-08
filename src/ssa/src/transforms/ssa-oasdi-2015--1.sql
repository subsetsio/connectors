SELECT
    CAST("State_Territory" AS VARCHAR) AS state,
    2015 AS year,
    CAST("Total_Beneficiaries" AS BIGINT) AS total,
    CAST("Retirement_Workers" AS BIGINT) AS retirement_workers,
    CAST("Retirement_Spouses" AS BIGINT) AS retirement_spouses,
    CAST("Retirement_Children" AS BIGINT) AS retirement_children,
    CAST("Survivors_Widowers_Parents" AS BIGINT) AS survivors_widowers_parents,
    CAST("Survivors_Children" AS BIGINT) AS survivors_children,
    CAST("Disability_Workers" AS BIGINT) AS disability_workers,
    CAST("Disability_Spouses" AS BIGINT) AS disability_spouses,
    CAST("Disability_Children" AS BIGINT) AS disability_children,
    CAST("Men65_Older" AS BIGINT) AS men_65_older,
    CAST("Women65_Older" AS BIGINT) AS women_65_older
FROM "ssa-oasdi-2015--1"
WHERE "State_Territory" IS NOT NULL AND TRIM(CAST("State_Territory" AS VARCHAR)) <> ''
