SELECT DISTINCT
    CAST(validFor AS DATE)         AS date,
    CAST(rate AS DOUBLE)           AS rate,
    CAST(volumeInCZKmio AS DOUBLE) AS volume_czk_mio
FROM "czech-national-bank-czeonia-daily"
WHERE validFor IS NOT NULL AND rate IS NOT NULL
