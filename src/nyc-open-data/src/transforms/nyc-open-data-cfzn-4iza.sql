-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bble",
    "bbl",
    "borough",
    "building_name",
    "street_address",
    "certification_class",
    "of_carriers",
    "coaxcable_connections",
    "fiber_connection",
    "satellitefixed_wireless_connection",
    "fiber_distribution",
    "isps",
    "multiple_points_of_entry",
    "designated_telecom_utility_space",
    "additional_telecom_space",
    "riser_space_for_current_providers",
    "riser_space_for_additional_providers",
    "diverse_riser_locations",
    "signed_poes",
    "agreements",
    "new_service_providers",
    "isps_1",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "postcode",
    "nta"
FROM "nyc-open-data-cfzn-4iza"
