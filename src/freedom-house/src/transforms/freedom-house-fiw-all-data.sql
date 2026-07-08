SELECT
    country_territory,
    region,
    ct,
    CAST(year AS INTEGER) AS year,
    status,
    pr_rating, cl_rating,
    a1, a2, a3, a,
    b1, b2, b3, b4, b,
    c1, c2, c3, c,
    add_q, add_a,
    pr_aggregate,
    d1, d2, d3, d4, d,
    e1, e2, e3, e,
    f1, f2, f3, f4, f,
    g1, g2, g3, g4, g,
    cl_aggregate,
    total
FROM "freedom-house-fiw-all-data"
WHERE country_territory IS NOT NULL AND year IS NOT NULL
