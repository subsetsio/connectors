SELECT
    CAST(TIME_PERIOD || '-01' AS DATE) AS month,
    REF_AREA                       AS country_code,
    ENERGY_PRODUCT                 AS product,
    FLOW_BREAKDOWN                 AS flow,
    UNIT_MEASURE                   AS unit,
    ASSESSMENT_CODE                AS assessment_code,
    TRY_CAST(OBS_VALUE AS DOUBLE)  AS value
FROM "jodi-oil-world-monthly"
WHERE TIME_PERIOD    IS NOT NULL
  AND REF_AREA       IS NOT NULL
  AND ENERGY_PRODUCT IS NOT NULL
  AND FLOW_BREAKDOWN IS NOT NULL
  AND TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
