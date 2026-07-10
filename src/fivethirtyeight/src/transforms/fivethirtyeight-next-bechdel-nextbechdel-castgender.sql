-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MOVIE" AS movie,
    "ACTOR" AS actor,
    "CHARACTER_NAME" AS character_name,
    "TYPE" AS type,
    "BILLING" AS billing,
    "GENDER" AS gender
FROM "fivethirtyeight-next-bechdel-nextbechdel-castgender"
