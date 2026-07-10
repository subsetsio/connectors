-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "URL" AS url,
    "Name/Alias" AS name_alias,
    "Appearances" AS appearances,
    "Current?" AS current,
    "Gender" AS gender,
    "Probationary Introl" AS probationary_introl,
    "Full/Reserve Avengers Intro" AS full_reserve_avengers_intro,
    "Year" AS year,
    "Years since joining" AS years_since_joining,
    "Honorary" AS honorary,
    "Death1" AS death1,
    "Return1" AS return1,
    "Death2" AS death2,
    "Return2" AS return2,
    "Death3" AS death3,
    "Return3" AS return3,
    "Death4" AS death4,
    "Return4" AS return4,
    "Death5" AS death5,
    "Return5" AS return5,
    "Notes" AS notes
FROM "fivethirtyeight-avengers-avengers"
