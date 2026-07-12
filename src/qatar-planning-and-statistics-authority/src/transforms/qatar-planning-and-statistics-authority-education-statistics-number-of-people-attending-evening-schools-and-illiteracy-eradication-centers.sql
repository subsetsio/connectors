-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "level_of_education",
    "lmrhl_lt_lymy",
    "gender",
    "lnw",
    "number_of_people_dd_l_shkhs"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-people-attending-evening-schools-and-illiteracy-eradication-centers"
