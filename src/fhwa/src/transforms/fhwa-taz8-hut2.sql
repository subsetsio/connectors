SELECT
    CAST(fiscal_year AS INTEGER)      AS fiscal_year,
    TRY_CAST(receipts AS BIGINT)      AS receipts,
    TRY_CAST(expenditures AS BIGINT)  AS expenditures,
    TRY_CAST(balance AS BIGINT)       AS balance
FROM "fhwa-taz8-hut2"
WHERE fiscal_year IS NOT NULL
  AND TRY_CAST(fiscal_year AS INTEGER) IS NOT NULL
