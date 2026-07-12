-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "preliminary_results"
FROM "qatar-planning-and-statistics-authority-health-risk-prevalence-data-stepwise-survey-2023"
