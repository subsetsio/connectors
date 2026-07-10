-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "AMONG ADULT MEN" AS among_adult_men,
    "C1" AS c1,
    "Adult Men" AS adult_men,
    "Age" AS age,
    "_1" AS 1,
    "_2" AS 2,
    "Race" AS race,
    "_3" AS 3,
    "Children" AS children,
    "_4" AS 4,
    "Sexual Orientation" AS sexual_orientation,
    "_5" AS 5
FROM "fivethirtyeight-masculinity-survey-masculinity-survey"
