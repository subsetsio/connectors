-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "cigarettes_shisha_counter_advertising",
    "nationality",
    "percentage_of_females",
    "percentage_of_males",
    "total_percentage"
FROM "qatar-planning-and-statistics-authority-cigarettes-and-shisha-industry-counter-advertising-by-nationality-and-gender"
