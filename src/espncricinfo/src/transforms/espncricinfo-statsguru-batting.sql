SELECT
    match_class,
    trim(regexp_replace(player, '\(.*\)', '')) AS player,
    regexp_extract(player, '\(([^)]+)\)', 1)   AS country,
    span,
    TRY_CAST(mat AS INTEGER)  AS matches,
    TRY_CAST(inns AS INTEGER) AS innings,
    TRY_CAST(no AS INTEGER)   AS not_outs,
    TRY_CAST(runs AS INTEGER) AS runs,
    hs                        AS highest_score,
    TRY_CAST(ave AS DOUBLE)   AS average,
    TRY_CAST(n100 AS INTEGER) AS hundreds,
    TRY_CAST(n50 AS INTEGER)  AS fifties,
    TRY_CAST(n0 AS INTEGER)   AS ducks
FROM "espncricinfo-statsguru-batting"
WHERE player IS NOT NULL
