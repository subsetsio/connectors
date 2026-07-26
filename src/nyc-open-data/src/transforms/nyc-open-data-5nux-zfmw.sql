-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date_year",
    "date_quarter",
    "total_applicants",
    "had_pet",
    "client_borough_of_entry_bronx",
    "client_borough_of_entry_manhattan",
    "client_borough_of_entry_brooklyn",
    "clients_who_would_have_entered_shelter_with_pet_if_allowed",
    "clients_choosing_to_forego_shelter",
    "chose_to_forego_shelter_for_how_many_days_avg",
    "clients_who_intend_to_regain_possession_upon_shelter_exit",
    "number_of_dogs",
    "number_of_cats",
    "number_of_birds",
    "number_of_small_mammals",
    "number_of_reptilessmall_amphibians",
    "number_of_fish",
    "did_not_report_pet_type",
    "pets_placed_with_foster_care_provider",
    "pets_surrendered_to_animal_shelter",
    "pets_placed_with_family",
    "pets_placed_with_friend",
    "pets_placed_with_other",
    "pets_placed_with_nonprofit"
FROM "nyc-open-data-5nux-zfmw"
