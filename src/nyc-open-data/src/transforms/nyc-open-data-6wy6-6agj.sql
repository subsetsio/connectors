-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "neighborhood_tabulation_area_code_nta_code",
    "neighborhood_tabulation_area_name_nta_name",
    "borough_name",
    "total_population",
    "total_number_of_households",
    "home_broadband_adoption_percentage_of_households",
    "home_broadband_adoption_by_quartiles_high_connected_medium_high_connected_medium_low_connected_low_connected",
    "mobile_broadband_adoption_percentage_of_households",
    "mobile_broadband_adoption_by_quartiles_high_connected_medium_high_connected_medium_low_connected_low_connected",
    "no_broadband_percentage_of_households",
    "no_broadand_by_quartiles_high_medium_high_medium_low_low",
    "commercial_fiber_max_isp_choice_by_nta",
    "percentage_of_blocks_without_a_commercial_fiber_provider",
    "percentage_of_blocks_without_a_commercial_fiber_provider_by_quartiles",
    "residential_broadband_isp_choice_average_by_nta",
    "residential_broadband_isp_choice_average_by_quartiles",
    "total_poles",
    "reserved_poles",
    "density_of_poles_reserved_and_with_equipment_installed_for_mobile_telecom_franchise",
    "public_wifi_in_nyc_count",
    "number_of_free_public_wifi_access_points_in_a_pedestrian_corridor",
    "available_free_public_wifi_in_a_pedestrian_corridor_yn",
    "number_of_public_computer_centers_with_free_public_wifi",
    "number_of_public_computer_center_workstations",
    "number_of_public_computer_center_open_lab_hours"
FROM "nyc-open-data-6wy6-6agj"
