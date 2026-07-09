-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Every column is a percentage rate, not an index level, and the `...YearOn` and `...Average` variants answer different questions (year-on-year change for the month vs the 12-month moving average). Never mix the two in one series.
-- caution: The CPI basket was rebased in 2025 (base year moved to 2024), so rates before and after that break are not computed on the same basket.
SELECT
    "id",
    "tyear",
    "tmonth",
    "period",
    CAST("allItemsYearOn" AS DOUBLE) AS allitemsyearon,
    CAST("allItemsAverage" AS DOUBLE) AS allitemsaverage,
    CAST("foodYearOn" AS DOUBLE) AS foodyearon,
    CAST("foodAverage" AS DOUBLE) AS foodaverage,
    CAST("allItemsLessFrmProdYearOn" AS DOUBLE) AS allitemslessfrmprodyearon,
    CAST("allItemsLessFrmProdAverage" AS DOUBLE) AS allitemslessfrmprodaverage,
    CAST("allItemsLessFrmProdAndEnergyYearOn" AS DOUBLE) AS allitemslessfrmprodandenergyyearon,
    CAST("allItemsLessFrmProdAndEnergyAvg" AS DOUBLE) AS allitemslessfrmprodandenergyavg
FROM "central-bank-of-nigeria-inflation-rates"
