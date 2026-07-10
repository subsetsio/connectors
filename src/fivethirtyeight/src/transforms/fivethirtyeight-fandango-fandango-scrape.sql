-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "FILM" AS film,
    "STARS" AS stars,
    "RATING" AS rating,
    "VOTES" AS votes
FROM "fivethirtyeight-fandango-fandango-scrape"
