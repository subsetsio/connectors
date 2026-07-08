SELECT
    TRY_CAST(fecha AS DATE)    AS date,
    moneda                     AS currency_code,
    nombre                     AS currency_name,
    codigo_iso                 AS iso_code,
    emisor                     AS issuer,
    CAST(tcc AS DOUBLE)        AS buy_rate,
    CAST(tcv AS DOUBLE)        AS sell_rate,
    CAST(arb_act AS DOUBLE)    AS arbitrage_factor,
    forma_arbitrar            AS arbitrage_form
FROM "central-bank-of-uruguay-exchange-rates"
WHERE TRY_CAST(fecha AS DATE) IS NOT NULL AND moneda IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY TRY_CAST(fecha AS DATE), moneda ORDER BY tcv DESC) = 1
