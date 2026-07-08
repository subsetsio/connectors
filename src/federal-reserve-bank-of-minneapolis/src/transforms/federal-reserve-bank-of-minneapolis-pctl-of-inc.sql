SELECT CAST(year AS INTEGER) AS year, * EXCLUDE (year)
FROM "federal-reserve-bank-of-minneapolis-pctl-of-inc"
WHERE year IS NOT NULL
