-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "number_of_completed_projects",
    "number_of_sites",
    "type_of_project"
FROM "qatar-planning-and-statistics-authority-public-infrastructure-and-buildings-construction-projects"
