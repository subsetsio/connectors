-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "building_id",
    "borough",
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
    "isps_1"
FROM "nyc-open-data-a6nj-cfbz"
