WITH ranked AS (
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
        table_title,
        row_number() OVER (
            PARTITION BY
                CASE WHEN section IS NULL OR section = ''
                     THEN item ELSE section || ' - ' || item END,
                period
            ORDER BY report_date DESC
        ) AS rn
    FROM "opec-table-11-3"
    WHERE value IS NOT NULL AND period IS NOT NULL
)
SELECT series, section, item, period, frequency, period_start,
       value, report_period, report_date, table_title
FROM ranked
WHERE rn = 1
ORDER BY series, period_start
