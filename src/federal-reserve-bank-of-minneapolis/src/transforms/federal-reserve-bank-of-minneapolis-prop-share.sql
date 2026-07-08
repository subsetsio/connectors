SELECT CAST(year AS INTEGER) AS year, * EXCLUDE (year)
FROM "federal-reserve-bank-of-minneapolis-prop-share"
WHERE year IS NOT NULL
