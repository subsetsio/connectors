-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "category",
    "facility_or_program_type",
    "families_with_children",
    "adult_families",
    "total_families",
    "total_adults_in_families",
    "total_children",
    "single_men",
    "single_women",
    "runaway_and_homeless_youth",
    "anyone_of_another_gender",
    "total_single_adults",
    "total_adults",
    "total",
    "data_period",
    "data_period_notes"
FROM "nyc-open-data-jiwc-ncpi"
