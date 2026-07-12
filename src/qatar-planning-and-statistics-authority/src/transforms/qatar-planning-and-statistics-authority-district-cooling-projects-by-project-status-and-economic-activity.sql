-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "economic_activity",
    "cooling_projects_operational_phase_no_of_projects",
    "cooling_projects_operational_phase_no_of_plants",
    "cooling_projects_under_construction",
    "cooling_projects_under_design"
FROM "qatar-planning-and-statistics-authority-district-cooling-projects-by-project-status-and-economic-activity"
