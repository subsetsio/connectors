SELECT DISTINCT
    TRY_CAST(effectiveDate AS DATE)      AS date,
    type                                 AS rate_type,
    TRY_CAST(percentRate AS DOUBLE)      AS rate_percent,
    TRY_CAST(percentPercentile1 AS DOUBLE)  AS percentile_1,
    TRY_CAST(percentPercentile25 AS DOUBLE) AS percentile_25,
    TRY_CAST(percentPercentile75 AS DOUBLE) AS percentile_75,
    TRY_CAST(percentPercentile99 AS DOUBLE) AS percentile_99,
    TRY_CAST(volumeInBillions AS DOUBLE) AS volume_billions,
    TRY_CAST(average30day AS DOUBLE)     AS average_30day,
    TRY_CAST(average90day AS DOUBLE)     AS average_90day,
    TRY_CAST(average180day AS DOUBLE)    AS average_180day,
    TRY_CAST("index" AS DOUBLE)          AS sofr_index
FROM "ny-fed-reference-rates-secured"
WHERE TRY_CAST(effectiveDate AS DATE) IS NOT NULL AND type IS NOT NULL
