-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "academic_year_of_graduation",
    "qatar",
    "international"
FROM "qatar-planning-and-statistics-authority-graduate-job-placement-by-location-and-academic-year"
