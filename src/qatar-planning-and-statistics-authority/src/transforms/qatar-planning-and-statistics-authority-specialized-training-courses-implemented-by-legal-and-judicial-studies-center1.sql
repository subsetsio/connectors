-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "year",
    "course_name",
    "course_type",
    "entity",
    "number_of_trainees",
    "males",
    "females",
    "start_date",
    "end_date",
    "descriptionnn"
FROM "qatar-planning-and-statistics-authority-specialized-training-courses-implemented-by-legal-and-judicial-studies-center1"
