-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FILM" AS film,
    "RottenTomatoes" AS rottentomatoes,
    "RottenTomatoes_User" AS rottentomatoes_user,
    "Metacritic" AS metacritic,
    "Metacritic_User" AS metacritic_user,
    "IMDB" AS imdb,
    "Fandango_Stars" AS fandango_stars,
    "Fandango_Ratingvalue" AS fandango_ratingvalue,
    "RT_norm" AS rt_norm,
    "RT_user_norm" AS rt_user_norm,
    "Metacritic_norm" AS metacritic_norm,
    "Metacritic_user_nom" AS metacritic_user_nom,
    "IMDB_norm" AS imdb_norm,
    "RT_norm_round" AS rt_norm_round,
    "RT_user_norm_round" AS rt_user_norm_round,
    "Metacritic_norm_round" AS metacritic_norm_round,
    "Metacritic_user_norm_round" AS metacritic_user_norm_round,
    "IMDB_norm_round" AS imdb_norm_round,
    "Metacritic_user_vote_count" AS metacritic_user_vote_count,
    "IMDB_user_vote_count" AS imdb_user_vote_count,
    "Fandango_votes" AS fandango_votes,
    "Fandango_Difference" AS fandango_difference
FROM "fivethirtyeight-fandango-fandango-score-comparison"
