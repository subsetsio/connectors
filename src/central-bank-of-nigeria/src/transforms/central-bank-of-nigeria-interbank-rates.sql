-- `weightedaverage` is space-padded in the source; TRIMmed before the cast
SELECT
    CAST("id" AS BIGINT) AS source_row_id,
    CAST("ratedate_iso" AS DATE) AS rate_date,
    NULLIF(TRIM("ratetype"), '') AS rate_type,
    NULLIF(TRIM("range"), '') AS rate_range,
    TRY_CAST(NULLIF(TRIM("weightedaverage"), '') AS DOUBLE) AS weighted_average_rate
FROM "central-bank-of-nigeria-interbank-rates"
