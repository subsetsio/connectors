SELECT
    db,
    series_code,
    frequency,
    -- survey_date width tracks frequency too (YYYYMMDD / YYYYMM /
    -- YYYY); parse robustly like the catalog so a single odd value
    -- can't abort the whole publish (strptime raises; try_strptime
    -- yields NULL).
    COALESCE(
        try_strptime(CAST(survey_date AS VARCHAR), '%Y%m%d'),
        try_strptime(CAST(survey_date AS VARCHAR), '%Y%m'),
        try_strptime(CAST(survey_date AS VARCHAR), '%Y')
    )::DATE AS date,
    CAST(value AS DOUBLE) AS value,
    COALESCE(
        try_strptime(CAST(last_update AS VARCHAR), '%Y%m%d'),
        try_strptime(CAST(last_update AS VARCHAR), '%Y%m'),
        try_strptime(CAST(last_update AS VARCHAR), '%Y')
    )::DATE AS last_update
FROM "bank-of-japan-values"
WHERE value IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY db, series_code, survey_date
    ORDER BY last_update DESC NULLS LAST
) = 1
