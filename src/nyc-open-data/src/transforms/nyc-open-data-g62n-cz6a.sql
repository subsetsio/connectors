-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "services_today",
    "other_services",
    "interpretation_services",
    "interpretation_language",
    "interpretation_language_other",
    "most_helpful",
    "recommend_fjc",
    "family_justice_center_fjc",
    "language_survey_completed"
FROM "nyc-open-data-g62n-cz6a"
