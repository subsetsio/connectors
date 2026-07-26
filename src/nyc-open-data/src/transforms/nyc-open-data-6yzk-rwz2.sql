-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "broadband_relationship_to_household_or_person_and_the_referenced_category",
    "home_broadband_adoption_all_nyc_households",
    "pecentage_of_home_broadband_adoption_all_nyc_households",
    "nyc_households_with_income_below_poverty_level",
    "percentage_of_nyc_households_with_income_below_poverty_level",
    "nyc_households_receiving_assistance_from_the_supplemental_nutrition_assistance_program",
    "percentage_of_nyc_households_receiving_assistance_from_the_supplemental_nutrition_assistance_program",
    "nyc_residents_without_a_high_school_degree",
    "percentage_of_nyc_residents_without_a_high_school_degree",
    "nyc_households_with_children_under_17_years_of_age",
    "percentage_of_nyc_households_with_children_under_17_years_of_age",
    "nyc_residents_who_are_blackafrican_american_or_of_hispanic_origin",
    "percentage_of_nyc_residents_who_are_blackafrican_american_or_of_hispanic_origin",
    "nyc_residents_who_speak_spanish_as_their_primary_language",
    "percentage_of_nyc_residents_who_speak_spanish_as_their_primary_language",
    "nyc_households_with_people_who_live_alone",
    "percentage_of_nyc_households_with_people_who_live_alone",
    "nyc_residents_65_years_old_and_older",
    "percentage_of_nyc_residents_65_years_old_and_older"
FROM "nyc-open-data-6yzk-rwz2"
