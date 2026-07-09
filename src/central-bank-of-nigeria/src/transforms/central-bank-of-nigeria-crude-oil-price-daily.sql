-- renamed from the source's camelCase; `postDate` parsed to a DATE via the download node's ISO twin
SELECT
    CAST("id" AS BIGINT) AS source_row_id,
    CAST("postDate_iso" AS DATE) AS post_date,
    TRY_CAST(NULLIF(TRIM("crudeOilPrice"), '') AS DOUBLE) AS crude_oil_price
FROM "central-bank-of-nigeria-crude-oil-price-daily"
