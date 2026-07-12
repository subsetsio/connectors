-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "cigarettes_shisha_advertising",
    "nationality",
    "percentage_of_non_smokers",
    "percentage_of_current_smokers",
    "overall_percentage"
FROM "qatar-planning-and-statistics-authority-cigarettes-and-shisha-industry-advertising-by-type-of-user"
