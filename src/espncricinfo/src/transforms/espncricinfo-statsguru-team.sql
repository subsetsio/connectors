SELECT
    match_class,
    team,
    span,
    TRY_CAST(mat AS INTEGER)  AS matches,
    TRY_CAST(won AS INTEGER)  AS won,
    TRY_CAST(lost AS INTEGER) AS lost,
    TRY_CAST(tied AS INTEGER) AS tied,
    TRY_CAST(draw AS INTEGER) AS drawn,
    TRY_CAST(w_l AS DOUBLE)   AS win_loss_ratio,
    TRY_CAST(ave AS DOUBLE)   AS average,
    TRY_CAST(rpo AS DOUBLE)   AS runs_per_over,
    TRY_CAST(inns AS INTEGER) AS innings,
    hs                        AS highest_score,
    ls                        AS lowest_score
FROM "espncricinfo-statsguru-team"
WHERE team IS NOT NULL
