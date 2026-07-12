-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_groups",
    "nationality",
    "illiterate",
    "read_write",
    "primary",
    "preparatory",
    "secondary",
    "pre_u_diploma",
    "university_and_above",
    "total"
FROM "qatar-planning-and-statistics-authority-female-economic-participation-rate-by-educational-status-and-age-group"
