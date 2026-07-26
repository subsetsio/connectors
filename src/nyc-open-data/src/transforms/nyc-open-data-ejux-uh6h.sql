-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "_quarter" AS quarter,
    "_location" AS location,
    "borough",
    "center",
    "nypd_called_on_scene",
    "employee_witnessed_an_nypd_arrest",
    "employee_witnessed_nypd_display_a_weapon_baton",
    "employee_witnessed_nypd_display_a_weapon_conducted_electrical_weapon",
    "employee_witnessed_nypd_display_a_weapon_firearm",
    "employee_witnessed_nypd_display_a_weapon_oleoresin_capsicum_spray",
    "employee_witnessed_nypd_display_a_weapon_other_weapon",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-ejux-uh6h"
