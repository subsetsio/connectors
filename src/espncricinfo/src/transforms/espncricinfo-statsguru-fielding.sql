SELECT
    match_class,
    trim(regexp_replace(player, '\(.*\)', '')) AS player,
    regexp_extract(player, '\(([^)]+)\)', 1)   AS country,
    span,
    TRY_CAST(mat AS INTEGER)  AS matches,
    TRY_CAST(inns AS INTEGER) AS innings,
    TRY_CAST(dis AS INTEGER)  AS dismissals,
    TRY_CAST(ct AS INTEGER)   AS caught,
    TRY_CAST(st AS INTEGER)   AS stumped,
    TRY_CAST(ct_wk AS INTEGER) AS caught_keeper,
    TRY_CAST(ct_fi AS INTEGER) AS caught_fielder,
    -- MD is formatted "N (Nct Mst)"; the leading integer is the
    -- max dismissals in an innings.
    TRY_CAST(regexp_extract(md, '^[0-9]+', 0) AS INTEGER) AS max_dismissals_innings,
    TRY_CAST(d_i AS DOUBLE)   AS dismissals_per_innings
FROM "espncricinfo-statsguru-fielding"
WHERE player IS NOT NULL
