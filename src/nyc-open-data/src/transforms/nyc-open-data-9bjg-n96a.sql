-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "oid",
    "state_senate_district",
    "home_broadband_adoption_percentage_of_households",
    "mobile_broadband_adoption_percentage_of_households",
    "no_internet_access_percentage_of_households",
    "no_home_broadband_adoption_percentage_of_households",
    "no_mobile_broadband_adoption_percentage_of_households",
    "no_home_broadband_adoption_by_quartile",
    "no_mobile_broadband_adoption_by_quartile",
    "commercial_fiber_max_isp_choice",
    "public_computer_center_count",
    "workstations_in_pccs",
    "avg_training_hrs_per_week_in_pccs",
    "public_wifi_count",
    "poles_reserved_by_mobile_telecom_franchisee",
    "pole_with_equipment_installed_by_mobile_telecom_franchise",
    "density_of_poles_reserved_and_with_equipment_installed_for_mobile_telecom_franchise"
FROM "nyc-open-data-9bjg-n96a"
