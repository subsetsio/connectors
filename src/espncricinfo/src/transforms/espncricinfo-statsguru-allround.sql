SELECT
    match_class,
    trim(regexp_replace(player, '\(.*\)', '')) AS player,
    regexp_extract(player, '\(([^)]+)\)', 1)   AS country,
    span,
    TRY_CAST(mat AS INTEGER)    AS matches,
    TRY_CAST(runs AS INTEGER)   AS runs,
    hs                          AS highest_score,
    TRY_CAST(bat_av AS DOUBLE)  AS batting_average,
    TRY_CAST(n100 AS INTEGER)   AS hundreds,
    TRY_CAST(wkts AS INTEGER)   AS wickets,
    bbi                         AS best_innings,
    TRY_CAST(bowl_av AS DOUBLE) AS bowling_average,
    TRY_CAST(n5 AS INTEGER)     AS five_wkts,
    TRY_CAST(ct AS INTEGER)     AS catches,
    TRY_CAST(st AS INTEGER)     AS stumpings,
    TRY_CAST(ave_diff AS DOUBLE) AS average_difference
FROM "espncricinfo-statsguru-allround"
WHERE player IS NOT NULL
