SELECT
    CAST(country_code AS BIGINT)  AS country_code,
    CAST(cancer_code  AS BIGINT)  AS cancer_code,
    CAST(sex          AS INTEGER) AS sex,
    CAST(type         AS INTEGER) AS measure_type,
    CASE WHEN CAST(type AS INTEGER) = 0 THEN 'incidence' ELSE 'mortality' END AS measure,
    CAST(year         AS INTEGER) AS year,
    CAST(cases_pred   AS DOUBLE)  AS cases_predicted,
    CAST(cases_base   AS DOUBLE)  AS cases_baseline,
    CAST(change       AS DOUBLE)  AS change,
    CAST(percent      AS DOUBLE)  AS percent_change
FROM "iarc-tomorrow-projections"
WHERE year IS NOT NULL AND cases_pred IS NOT NULL
