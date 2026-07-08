SELECT
    CAST("State_Territory" AS VARCHAR) AS state,
    2013 AS year,
    CAST("Total" AS BIGINT) AS total,
    CAST("Retirement_retired_workers" AS BIGINT) AS retirement_workers,
    CAST("Retirement_spouses" AS BIGINT) AS retirement_spouses,
    CAST("Retirement_children" AS BIGINT) AS retirement_children,
    CAST("Survivors_widowers_and_parents" AS BIGINT) AS survivors_widowers_parents,
    CAST("Survivors_children" AS BIGINT) AS survivors_children,
    CAST("Disability_disabled_workers" AS BIGINT) AS disability_workers,
    CAST("Disability_spouses" AS BIGINT) AS disability_spouses,
    CAST("Disability_children" AS BIGINT) AS disability_children,
    CAST("Aged65_or_older_men" AS BIGINT) AS men_65_older,
    CAST("Aged65_or_older_women" AS BIGINT) AS women_65_older
FROM "ssa-oasdi--2013--2"
WHERE "State_Territory" IS NOT NULL AND TRIM(CAST("State_Territory" AS VARCHAR)) <> ''
