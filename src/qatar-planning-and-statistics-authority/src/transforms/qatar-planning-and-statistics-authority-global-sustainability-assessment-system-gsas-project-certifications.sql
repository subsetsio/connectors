-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "certification_type",
    "certification_level",
    "number_of_projects"
FROM "qatar-planning-and-statistics-authority-global-sustainability-assessment-system-gsas-project-certifications"
