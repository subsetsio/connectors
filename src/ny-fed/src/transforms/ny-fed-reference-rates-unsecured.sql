SELECT DISTINCT
    TRY_CAST(effectiveDate AS DATE)      AS date,
    type                                 AS rate_type,
    TRY_CAST(percentRate AS DOUBLE)      AS rate_percent,
    TRY_CAST(percentPercentile1 AS DOUBLE)  AS percentile_1,
    TRY_CAST(percentPercentile25 AS DOUBLE) AS percentile_25,
    TRY_CAST(percentPercentile75 AS DOUBLE) AS percentile_75,
    TRY_CAST(percentPercentile99 AS DOUBLE) AS percentile_99,
    TRY_CAST(volumeInBillions AS DOUBLE) AS volume_billions,
    TRY_CAST(targetRateFrom AS DOUBLE)   AS target_rate_from,
    TRY_CAST(targetRateTo AS DOUBLE)     AS target_rate_to
FROM "ny-fed-reference-rates-unsecured"
WHERE TRY_CAST(effectiveDate AS DATE) IS NOT NULL AND type IS NOT NULL
