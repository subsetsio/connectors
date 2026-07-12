-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "gulf",
    "arab",
    "asian",
    "international",
    "total"
FROM "qatar-planning-and-statistics-authority-overseas-meetings-conferences-and-forums-by-implementation-level-2017-2022"
