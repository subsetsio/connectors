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
    "OpeningTags"                  AS opening_tags
FROM "lichess-puzzles"
WHERE "PuzzleId" IS NOT NULL
