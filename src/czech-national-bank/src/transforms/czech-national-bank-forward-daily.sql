SELECT DISTINCT
    CAST(validFor AS DATE)         AS date,
    ccyPair                        AS currency_pair,
    maturity,
    CAST(forwardPoints AS DOUBLE)  AS forward_points
FROM "czech-national-bank-forward-daily"
WHERE validFor IS NOT NULL AND forwardPoints IS NOT NULL
