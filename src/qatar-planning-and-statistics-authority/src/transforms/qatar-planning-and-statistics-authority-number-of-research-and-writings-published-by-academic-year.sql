-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "academic_year",
    "research_and_writings_published"
FROM "qatar-planning-and-statistics-authority-number-of-research-and-writings-published-by-academic-year"
