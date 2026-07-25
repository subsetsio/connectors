-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "agency",
    "city",
    "state",
    "ntd_id",
    "organization_type",
    "reporter_type",
    CAST("report_year" AS BIGINT) AS report_year,
    "uace_code",
    "uza_name",
    CAST("primary_uza_population" AS BIGINT) AS primary_uza_population,
    CAST("agency_voms" AS BIGINT) AS agency_voms,
    CAST("maintenance_facility_service" AS BIGINT) AS maintenance_facility_service,
    CAST("heavy_maintenance_overhaul" AS BIGINT) AS heavy_maintenance_overhaul,
    CAST("general_purpose_maintenance" AS BIGINT) AS general_purpose_maintenance,
    CAST("vehicle_washing_facility" AS BIGINT) AS vehicle_washing_facility,
    CAST("vehicle_blow_down_facility" AS BIGINT) AS vehicle_blow_down_facility,
    CAST("vehicle_fueling_facility" AS BIGINT) AS vehicle_fueling_facility,
    CAST("vehicle_testing_facility" AS BIGINT) AS vehicle_testing_facility,
    CAST("maintenance_facilities" AS BIGINT) AS maintenance_facilities,
    CAST("administrative_office_sales" AS BIGINT) AS administrative_office_sales,
    CAST("revenue_collection_facility" AS BIGINT) AS revenue_collection_facility,
    CAST("combined_administrative_and" AS BIGINT) AS combined_administrative_and,
    CAST("other_administrative" AS BIGINT) AS other_administrative,
    CAST("administrative_and_other_non_passenger_facilities" AS BIGINT) AS administrative_and_other_non_passenger_facilities,
    CAST("bus_transfer_center" AS BIGINT) AS bus_transfer_center,
    CAST("elevated_fixed_guideway" AS BIGINT) AS elevated_fixed_guideway,
    CAST("at_grade_fixed_guideway" AS BIGINT) AS at_grade_fixed_guideway,
    CAST("underground_fixed_guideway" AS BIGINT) AS underground_fixed_guideway,
    CAST("simple_at_grade_platform" AS BIGINT) AS simple_at_grade_platform,
    CAST("exclusive_grade_separated" AS BIGINT) AS exclusive_grade_separated,
    CAST("ferryboat_terminal" AS BIGINT) AS ferryboat_terminal,
    CAST("passenger_stations_and_terminals" AS BIGINT) AS passenger_stations_and_terminals,
    CAST("surface_parking_lot" AS BIGINT) AS surface_parking_lot,
    CAST("parking_structure" AS BIGINT) AS parking_structure,
    CAST("other_passenger_or_parking" AS BIGINT) AS other_passenger_or_parking,
    CAST("parking_and_other_passenger_facilities" AS BIGINT) AS parking_and_other_passenger_facilities,
    CAST("total_facilities" AS BIGINT) AS total_facilities
FROM "u-s-department-of-transportation-aqct-knjk"
