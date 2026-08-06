SELECT
    "PuzzleId"                     AS puzzle_id,
    "FEN"                          AS fen,
    "Moves"                        AS moves,
    CAST("Rating"          AS INTEGER) AS rating,
    CAST("RatingDeviation" AS INTEGER) AS rating_deviation,
    CAST("Popularity"      AS INTEGER) AS popularity,
    CAST("NbPlays"         AS BIGINT)  AS nb_plays,
    "Themes"                       AS themes,
    "GameUrl"                      AS game_url,
    "OpeningTags"                  AS opening_tags,
    CAST("DailyDate"       AS BIGINT)  AS daily_date_ms,
    CASE
        WHEN "DailyDate" IS NULL THEN NULL
        ELSE CAST(to_timestamp(CAST("DailyDate" AS DOUBLE) / 1000.0) AS TIMESTAMP)
    END                            AS daily_date
FROM "lichess-puzzles"
WHERE "PuzzleId" IS NOT NULL
