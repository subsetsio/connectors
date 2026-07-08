SELECT
    CAST(date AS DATE) AS date,
    mnemonic,
    CAST(value AS DOUBLE) AS value
FROM "ofr-fpf"
WHERE value IS NOT NULL AND date IS NOT NULL
