-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "tobacco_industry_counter_advertising",
    "percentage_of_non_smokers_users",
    "percentage_of_current_smokers_users",
    "total_percentage"
FROM "qatar-planning-and-statistics-authority-tobacco-industry-counter-advertising-by-type-of-users"
