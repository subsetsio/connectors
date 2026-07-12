-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "quarter",
    "lrb",
    "place_of_death",
    "mkn_lwf",
    "male",
    "female",
    "total"
FROM "qatar-planning-and-statistics-authority-registered-qatari-deaths-by-gender-and-place-of-death"
