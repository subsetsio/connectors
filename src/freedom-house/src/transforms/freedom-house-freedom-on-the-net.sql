SELECT
    country,
    CAST(year AS INTEGER) AS year,
    status,
    a1, a2, a3, a4, a5, a,
    b1, b2, b3, b4, b5, b6, b7, b8, b,
    c1, c2, c3, c4, c5, c6, c7, c8, c,
    total
FROM "freedom-house-freedom-on-the-net"
WHERE country IS NOT NULL AND year IS NOT NULL
