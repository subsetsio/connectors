SELECT
    CAST(release_date AS DATE)   AS release_date,
    gender,
    CAST(rank AS INTEGER)        AS rank,
    id_team,
    team_name,
    country_code,
    CAST(total_points AS DOUBLE) AS total_points,
    CAST(previous_rank AS INTEGER) AS previous_rank,
    CAST(previous_points AS DOUBLE) AS previous_points,
    confederation
FROM "fifa-women-world-ranking"
WHERE release_date IS NOT NULL
  AND id_team IS NOT NULL
  AND rank IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY release_date, id_team ORDER BY rank
) = 1
