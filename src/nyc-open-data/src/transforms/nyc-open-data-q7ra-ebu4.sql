-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "borough_of_building",
    "district_of_building",
    "building_code",
    "formatting",
    "building_name",
    "building_level",
    "building_enrollment_based_on_20132014_blue_book",
    "building_capacity_based_on_20132014_blue_book",
    "school_code",
    "school_name",
    "final_uu_2015_designation"
FROM "nyc-open-data-q7ra-ebu4"
