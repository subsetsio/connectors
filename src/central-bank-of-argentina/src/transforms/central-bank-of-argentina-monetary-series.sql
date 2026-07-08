SELECT
    CAST(idVariable AS BIGINT)               AS variable_id,
    descripcion                              AS description,
    categoria                                AS category,
    tipoSerie                                AS series_type,
    periodicidad                             AS frequency,
    unidadExpresion                          AS unit,
    moneda                                   AS currency,
    TRY_CAST(primerFechaInformada AS DATE)   AS first_date,
    TRY_CAST(ultFechaInformada AS DATE)      AS last_date,
    CAST(ultValorInformado AS DOUBLE)        AS last_value
FROM "central-bank-of-argentina-monetary-series"
WHERE idVariable IS NOT NULL
