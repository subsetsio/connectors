-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MOVIE" AS movie,
    "DEPARTMENT" AS department,
    "FULL_NAME" AS full_name,
    "FIRST_NAME" AS first_name,
    "IMDB" AS imdb,
    "GENDER_PROB" AS gender_prob,
    "GENDER_GUESS" AS gender_guess
FROM "fivethirtyeight-next-bechdel-nextbechdel-crewgender"
