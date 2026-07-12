-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "economic_activity",
    "economic_activity_ar",
    "cooling_projects_operational_phase",
    "cooling_projects_under_construction",
    "cooling_projects_under_design"
FROM "qatar-planning-and-statistics-authority-the-capacity-of-the-design-cooling-plants-for-district-cooling-projects-by-the-project-status-and-economic-activity-cooling-tons"
