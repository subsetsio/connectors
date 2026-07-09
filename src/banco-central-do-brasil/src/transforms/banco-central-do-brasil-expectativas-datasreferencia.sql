SELECT
    CAST(Indicador AS VARCHAR)        AS Indicador,
    CAST(periodo AS VARCHAR)          AS periodo,
    TRY_CAST(DataReferencia1 AS DATE) AS DataReferencia1,
    TRY_CAST(DataReferencia2 AS DATE) AS DataReferencia2
FROM "banco-central-do-brasil-expectativas-datasreferencia"
