SELECT DISTINCT
    codigoMoneda             AS currency_code,
    descripcion              AS currency_name,
    CAST(fecha AS DATE)      AS date,
    CAST(tipoPase AS DOUBLE) AS rate_vs_usd,
    CAST(tipoCotizacion AS DOUBLE) AS rate_in_pesos
FROM "central-bank-of-argentina-fx-quotations"
WHERE fecha IS NOT NULL AND tipoCotizacion IS NOT NULL
