SELECT
    make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
    CAST(year AS INTEGER) AS year,
    CAST(month AS INTEGER) AS month,
    "group" AS rank_group,
    unit,
    date AS source_date,
    CAST(pop_adults AS DOUBLE) AS pop_adults,
    CAST(pop_working_age AS DOUBLE) AS pop_working_age,
    CAST(housing AS DOUBLE) AS housing,
    CAST(equity AS DOUBLE) AS equity,
    CAST(other AS DOUBLE) AS other,
    CAST(wealth AS DOUBLE) AS wealth
FROM "realtime-inequality-wealth-projection"
WHERE year IS NOT NULL
  AND month IS NOT NULL
  AND "group" IS NOT NULL
  AND unit IS NOT NULL
