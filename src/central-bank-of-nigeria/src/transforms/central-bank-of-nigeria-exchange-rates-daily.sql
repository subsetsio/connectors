-- `currency` is TRIMmed only — the trailing tabs and spaces are transport noise; the naming variants are NOT merged, which would be an editorial judgement about the source
SELECT
    CAST("id" AS BIGINT) AS source_row_id,
    CAST("ratedate" AS DATE) AS rate_date,
    NULLIF(TRIM("currency"), '') AS currency,
    TRY_CAST(NULLIF(TRIM("buyingrate"), '') AS DOUBLE) AS buying_rate,
    TRY_CAST(NULLIF(TRIM("centralrate"), '') AS DOUBLE) AS central_rate,
    TRY_CAST(NULLIF(TRIM("sellingrate"), '') AS DOUBLE) AS selling_rate
FROM "central-bank-of-nigeria-exchange-rates-daily"
