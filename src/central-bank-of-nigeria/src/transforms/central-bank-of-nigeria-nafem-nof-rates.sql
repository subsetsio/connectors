-- `nofr` renamed `nof_rate`; the rate columns are percentages, NOT naira-per-dollar exchange rates
SELECT
    CAST("id" AS BIGINT) AS source_row_id,
    CAST("ratedate_iso" AS DATE) AS rate_date,
    TRY_CAST(NULLIF(TRIM("dailyVolume"), '') AS DOUBLE) AS daily_volume,
    TRY_CAST(NULLIF(TRIM("minimumRate"), '') AS DOUBLE) AS minimum_rate,
    TRY_CAST(NULLIF(TRIM("maximumRate"), '') AS DOUBLE) AS maximum_rate,
    TRY_CAST(NULLIF(TRIM("dailyVariationRange"), '') AS DOUBLE) AS daily_variation_range,
    TRY_CAST(NULLIF(TRIM("nofr"), '') AS DOUBLE) AS nof_rate
FROM "central-bank-of-nigeria-nafem-nof-rates"
