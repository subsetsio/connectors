SELECT
    CAST(simbolo AS VARCHAR)       AS simbolo,
    CAST(nomeFormatado AS VARCHAR) AS nomeFormatado,
    CAST(tipoMoeda AS VARCHAR)     AS tipoMoeda
FROM "banco-central-do-brasil-ptax-moedas"
