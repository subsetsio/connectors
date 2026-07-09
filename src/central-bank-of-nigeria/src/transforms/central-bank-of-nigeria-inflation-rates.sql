-- `allItemsLessFrmProd*` renamed to the standard `core_*`: CBN's "all items less farm produce" IS the core index
-- `id` and the `period` label are dropped: (year, month) is the source's real grain
SELECT
    CAST("period_start_iso" AS DATE) AS month_start,
    CAST("tyear" AS BIGINT) AS year,
    CAST("tmonth" AS BIGINT) AS month,
    TRY_CAST(NULLIF(TRIM("allItemsYearOn"), '') AS DOUBLE) AS all_items_yoy,
    TRY_CAST(NULLIF(TRIM("allItemsAverage"), '') AS DOUBLE) AS all_items_12m_average,
    TRY_CAST(NULLIF(TRIM("foodYearOn"), '') AS DOUBLE) AS food_yoy,
    TRY_CAST(NULLIF(TRIM("foodAverage"), '') AS DOUBLE) AS food_12m_average,
    TRY_CAST(NULLIF(TRIM("allItemsLessFrmProdYearOn"), '') AS DOUBLE) AS core_yoy,
    TRY_CAST(NULLIF(TRIM("allItemsLessFrmProdAverage"), '') AS DOUBLE) AS core_12m_average,
    TRY_CAST(NULLIF(TRIM("allItemsLessFrmProdAndEnergyYearOn"), '') AS DOUBLE) AS core_less_energy_yoy,
    TRY_CAST(NULLIF(TRIM("allItemsLessFrmProdAndEnergyAvg"), '') AS DOUBLE) AS core_less_energy_12m_average
FROM "central-bank-of-nigeria-inflation-rates"
