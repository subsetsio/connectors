-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "adults",
    "youth",
    "junior_under_18",
    "junior_under_16",
    "kids"
FROM "qatar-planning-and-statistics-authority-international-championships-by-age-groups"
