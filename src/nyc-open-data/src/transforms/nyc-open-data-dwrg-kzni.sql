-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date_of_census",
    "total_adults_in_shelter",
    "total_children_in_shelter",
    "total_individuals_in_shelter",
    "single_adult_men_in_shelter",
    "single_adult_women_in_shelter",
    "total_single_adults_in_shelter",
    "families_with_children_in_shelter",
    "adults_in_families_with_children_in_shelter",
    "children_in_families_with_children_in_shelter",
    "total_individuals_in_families_with_children_in_shelter",
    "adult_families_in_shelter",
    "individuals_in_adult_families_in_shelter"
FROM "nyc-open-data-dwrg-kzni"
