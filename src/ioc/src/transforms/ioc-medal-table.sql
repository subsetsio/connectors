SELECT
    edition,
    games,
    noc_code,
    noc_name,
    sport,
    gender,
    CAST(gold   AS BIGINT) AS gold,
    CAST(silver AS BIGINT) AS silver,
    CAST(bronze AS BIGINT) AS bronze,
    CAST(total  AS BIGINT) AS total,
    CAST(rank   AS BIGINT) AS rank,
    CAST(rank_total AS BIGINT) AS rank_total
FROM "ioc-medal-table"
WHERE noc_code IS NOT NULL
  AND sport IS NOT NULL
  AND gender IS NOT NULL
