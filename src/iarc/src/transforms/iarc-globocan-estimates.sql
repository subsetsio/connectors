SELECT
    CAST(country_code AS BIGINT)  AS country_code,
    CAST(cancer_code  AS BIGINT)  AS cancer_code,
    CAST(sex          AS INTEGER) AS sex,
    CAST(type         AS INTEGER) AS measure_type,
    CASE WHEN CAST(type AS INTEGER) = 0 THEN 'incidence' ELSE 'mortality' END AS measure,
    CAST(total        AS BIGINT)  AS cases,
    CAST(total_pop    AS BIGINT)  AS population,
    CAST(asr          AS DOUBLE)  AS asr,
    CAST(crude_rate   AS DOUBLE)  AS crude_rate,
    CAST(cum_risk_74  AS DOUBLE)  AS cum_risk_74,
    CAST(ui_low       AS BIGINT)  AS ui_low,
    CAST(ui_high      AS BIGINT)  AS ui_high
FROM "iarc-globocan-estimates"
WHERE total IS NOT NULL
