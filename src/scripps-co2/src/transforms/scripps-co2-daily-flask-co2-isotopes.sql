SELECT station,
       CAST(date AS DATE)           AS date,
       CAST(decimal_date AS DOUBLE) AS decimal_date,
       CASE WHEN CAST(co2_flag AS INTEGER) <= 0 THEN CAST(co2 AS DOUBLE) END         AS co2,
       CASE WHEN CAST(ch4_flag AS INTEGER) <= 0 THEN CAST(ch4 AS DOUBLE) END         AS ch4,
       CASE WHEN CAST(co_flag AS INTEGER)  <= 0 THEN CAST(co AS DOUBLE) END          AS co,
       CASE WHEN CAST(c13_flag AS INTEGER) <= 0 THEN CAST(c13_co2 AS DOUBLE) END     AS c13_co2,
       CASE WHEN CAST(o18_flag AS INTEGER) <= 0 THEN CAST(o18_co2 AS DOUBLE) END     AS o18_co2,
       CASE WHEN CAST(c14_flag AS INTEGER) <= 0 THEN CAST(c14_co2 AS DOUBLE) END     AS c14_co2
FROM "scripps-co2-daily-flask-co2-isotopes"
WHERE COALESCE(
          CASE WHEN CAST(co2_flag AS INTEGER) <= 0 THEN co2 END,
          CASE WHEN CAST(ch4_flag AS INTEGER) <= 0 THEN ch4 END,
          CASE WHEN CAST(co_flag AS INTEGER)  <= 0 THEN co END,
          CASE WHEN CAST(c13_flag AS INTEGER) <= 0 THEN c13_co2 END,
          CASE WHEN CAST(o18_flag AS INTEGER) <= 0 THEN o18_co2 END,
          CASE WHEN CAST(c14_flag AS INTEGER) <= 0 THEN c14_co2 END
      ) IS NOT NULL
