SELECT DISTINCT
    state,
    district,
    market,
    commodity,
    variety,
    grade,
    try_strptime(arrival_date, '%d/%m/%Y')::DATE AS arrival_date,
    TRY_CAST(min_price   AS DOUBLE) AS min_price,
    TRY_CAST(max_price   AS DOUBLE) AS max_price,
    TRY_CAST(modal_price AS DOUBLE) AS modal_price
FROM "agmarknet-prices"
WHERE try_strptime(arrival_date, '%d/%m/%Y') IS NOT NULL
