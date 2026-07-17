-- caution: Rows combine observations from many BOJ databases and reporting frequencies; aggregate only after filtering to comparable series or grouping by db, series_code, and frequency.
-- caution: The date column normalizes daily, monthly, quarterly, and annual BOJ survey dates to calendar dates, defaulting missing month/day components to the first day.
SELECT
    db,
    series_code,
    frequency,
    -- survey_date width tracks frequency too (YYYYMMDD / YYYYMM /
    -- YYYY). Use integer ranges instead of trying every date format
    -- for every row; this table is tens of millions of observations.
    CASE
        WHEN survey_date BETWEEN 10000000 AND 99991231
            THEN try_strptime(CAST(survey_date AS VARCHAR), '%Y%m%d')::DATE
        WHEN survey_date BETWEEN 100000 AND 999912
            THEN try_strptime(CAST(survey_date AS VARCHAR), '%Y%m')::DATE
        WHEN survey_date BETWEEN 1000 AND 9999
            THEN make_date(survey_date, 1, 1)
        ELSE NULL
    END AS date,
    CAST(value AS DOUBLE) AS value,
    CASE
        WHEN last_update BETWEEN 10000000 AND 99991231
            THEN try_strptime(CAST(last_update AS VARCHAR), '%Y%m%d')::DATE
        WHEN last_update BETWEEN 100000 AND 999912
            THEN try_strptime(CAST(last_update AS VARCHAR), '%Y%m')::DATE
        WHEN last_update BETWEEN 1000 AND 9999
            THEN make_date(last_update, 1, 1)
        ELSE NULL
    END AS last_update
FROM "bank-of-japan-values"
WHERE value IS NOT NULL
