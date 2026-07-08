SELECT
    TRIM("CODE")                                          AS code,
    TRIM("MFR")                                           AS mfr,
    TRIM("MODEL")                                         AS model,
    TRIM("TYPE")                                          AS type,
    TRY_CAST(NULLIF(TRIM("HORSEPOWER"), '') AS INTEGER)   AS horsepower,
    TRY_CAST(NULLIF(TRIM("THRUST"), '') AS INTEGER)       AS thrust_lbs
FROM "faa-engine"
WHERE TRIM("CODE") <> ''
