SELECT
    CAST(country_code AS BIGINT)  AS country_code,
    CAST(cancer_code  AS BIGINT)  AS cancer_code,
    CAST(sex          AS INTEGER) AS sex,
    CAST(type         AS INTEGER) AS measure_type,
    CASE WHEN CAST(type AS INTEGER) = 0 THEN 'incidence' ELSE 'mortality' END AS measure,
    CAST(year         AS INTEGER) AS year,
    CAST(cases        AS BIGINT)  AS cases,
    CAST(person_years AS BIGINT)  AS person_years,
    CASE WHEN CAST(person_years AS DOUBLE) > 0
         THEN CAST(cases AS DOUBLE) / CAST(person_years AS DOUBLE) * 100000
    END                           AS crude_rate_per_100k
FROM "iarc-overtime-rates"
WHERE year IS NOT NULL AND person_years > 0
