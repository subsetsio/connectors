SELECT
    CAST(y0 AS INTEGER) AS y0,
    CAST(y1 AS INTEGER) AS y1,
    * EXCLUDE (y0, y1)
FROM "federal-reserve-bank-of-minneapolis-inc-change-distributions"
WHERE y0 IS NOT NULL AND y1 IS NOT NULL
