SELECT
    TRY_CAST(TRIM(AOU) AS INTEGER) AS aou,
    TRIM(Region)                    AS region,
    TRY_CAST(TRIM(Year) AS INTEGER) AS year,
    TRY_CAST(TRIM("Index") AS DOUBLE)   AS annual_index,
    TRY_CAST(TRIM("2.5%CI") AS DOUBLE)  AS ci_lower,
    TRY_CAST(TRIM("97.5%CI") AS DOUBLE) AS ci_upper
FROM "north-american-breeding-bird-survey-analysis-core-indices"
WHERE TRIM(AOU) <> '' AND TRIM(Year) <> ''
