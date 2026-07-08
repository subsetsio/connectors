SELECT CAST(date AS DATE)            AS date,
       CAST(year AS INTEGER)         AS year,
       CAST(change_in_opr AS DOUBLE) AS change_in_opr,
       CAST(new_opr_level AS DOUBLE) AS new_opr_level
FROM "bank-negara-malaysia-opr"
WHERE date IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY date ORDER BY date) = 1
