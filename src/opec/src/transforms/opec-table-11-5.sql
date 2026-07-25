SELECT series, section, item, period, frequency, period_start,
       value, report_period, report_date, table_title
FROM (
    SELECT
        CASE WHEN section IS NULL OR section = ''
             THEN item ELSE section || ' - ' || item END  AS series,
        section,
        item,
        period,
        frequency,
        CAST(period_start AS DATE)  AS period_start,
        CAST(value AS DOUBLE)       AS value,
        report_period,
        CAST(report_date AS DATE)   AS report_date,
        table_title
    FROM "opec-table-11-5"
    WHERE value IS NOT NULL AND period IS NOT NULL
)
ORDER BY report_date, period_start, series, period
