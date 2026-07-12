-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "work_category",
    "work_type",
    "unit",
    "value"
FROM "qatar-planning-and-statistics-authority-completed-infrastructure-projects-by-work-category-type-and-year"
