-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "lastname",
    "usename",
    "fullname",
    "birthdate",
    "birthcity",
    "birthstate",
    "birthcountry",
    "deathdate",
    "deathcity",
    "deathstate",
    "deathcountry",
    "cemetery",
    "cem_city",
    "cem_state",
    "cem_ctry",
    "cem_note",
    "birthname",
    "altname",
    "debut_p",
    "last_p",
    "debut_c",
    "last_c",
    "debut_m",
    "last_m",
    "debut_u",
    "last_u",
    "bats",
    "throws",
    "height",
    "weight",
    "HOF" AS hof
FROM "retrosheet-biofile"
