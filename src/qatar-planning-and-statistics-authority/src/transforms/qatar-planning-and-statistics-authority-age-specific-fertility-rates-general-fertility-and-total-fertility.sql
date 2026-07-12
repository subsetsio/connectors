-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "ljnsy",
    "general_fertility_rate_per_1000_women",
    "total_fertility_rate_per_woman",
    "gross_reproduction_rate",
    "average_age_of_child_bearing"
FROM "qatar-planning-and-statistics-authority-age-specific-fertility-rates-general-fertility-and-total-fertility"
