SELECT
    match_class,
    trim(regexp_replace(player, '\(.*\)', '')) AS player,
    regexp_extract(player, '\(([^)]+)\)', 1)   AS country,
    span,
    TRY_CAST(mat AS INTEGER)   AS matches,
    TRY_CAST(inns AS INTEGER)  AS innings,
    TRY_CAST(balls AS INTEGER) AS balls,
    TRY_CAST(runs AS INTEGER)  AS runs_conceded,
    TRY_CAST(wkts AS INTEGER)  AS wickets,
    bbi                        AS best_innings,
    bbm                        AS best_match,
    TRY_CAST(ave AS DOUBLE)    AS average,
    TRY_CAST(econ AS DOUBLE)   AS economy,
    TRY_CAST(sr AS DOUBLE)     AS strike_rate,
    TRY_CAST(n5 AS INTEGER)    AS five_wkts,
    TRY_CAST(n10 AS INTEGER)   AS ten_wkts
FROM "espncricinfo-statsguru-bowling"
WHERE player IS NOT NULL
