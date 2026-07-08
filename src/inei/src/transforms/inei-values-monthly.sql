SELECT
    indicador_id,
    anio AS year,
    CAST(SUBSTR(month_col, 2) AS INTEGER) AS month,
    make_date(anio, CAST(SUBSTR(month_col, 2) AS INTEGER), 1) AS date,
    value
FROM (
    UNPIVOT "inei-values-monthly"
    ON m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12
    INTO NAME month_col VALUE value
) AS u
WHERE value IS NOT NULL
  AND value NOT BETWEEN -10000000000.0 AND -9999999999.0 AND value NOT BETWEEN -8888888889.0 AND -8888888888.0
