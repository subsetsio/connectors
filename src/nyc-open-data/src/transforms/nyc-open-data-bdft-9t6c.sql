-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "reporting_requirements",
    "category",
    "facility_or_program_type",
    "families_with_children",
    "adult_families",
    "total_families",
    "total_adults_on_families",
    "total_children",
    "single_men",
    "single_women",
    "total_single_adults",
    "total_adults",
    "data_period"
FROM "nyc-open-data-bdft-9t6c"
