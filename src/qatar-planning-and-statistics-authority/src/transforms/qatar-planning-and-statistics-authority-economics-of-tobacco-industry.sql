-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "economics_of_the_tobacco_industry",
    "unit",
    "value"
FROM "qatar-planning-and-statistics-authority-economics-of-tobacco-industry"
