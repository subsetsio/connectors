-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table is wide across transport measures; each measure column has its own unit and should not be summed across columns.
SELECT
    CAST("Year" AS BIGINT) AS year,
    CAST("Length of roads (km)" AS BIGINT) AS length_of_roads_km,
    CAST("Vehicles per km of road" AS BIGINT) AS vehicles_per_km_of_road,
    CAST("Road density (km of road per sq. km of land area) per sq. km" AS DOUBLE) AS road_density_km_of_road_per_sq_km_of_land_area_per_sq_km,
    CAST("% Roads, paved (% of total roads)" AS BIGINT) AS roads_paved_of_total_roads,
    CAST("Number of Motor vehicles per 1,000 people" AS BIGINT) AS number_of_motor_vehicles_per_1_000_people,
    CAST("Number of Passenger cars per 1,000 people" AS BIGINT) AS number_of_passenger_cars_per_1_000_people,
    CAST("Number of Vehicles registered" AS BIGINT) AS number_of_vehicles_registered,
    CAST("Number of New Vehicles registered" AS BIGINT) AS number_of_new_vehicles_registered,
    CAST("Number of Imported second-hand Vehicles registered" AS BIGINT) AS number_of_imported_second_hand_vehicles_registered,
    CAST("Number of Re-registered Vehicles" AS BIGINT) AS number_of_re_registered_vehicles,
    CAST("Number of Vehicles off the road" AS BIGINT) AS number_of_vehicles_off_the_road,
    CAST("Number of Road Traffic Accidents" AS BIGINT) AS number_of_road_traffic_accidents,
    CAST("Number of  Casualty Road Traffic Accidents" AS BIGINT) AS number_of_casualty_road_traffic_accidents,
    CAST("Number of Non InjuryRoad Traffic Accidents" AS BIGINT) AS number_of_non_injuryroad_traffic_accidents,
    CAST("Number of Vehicles involved in road accidents" AS BIGINT) AS number_of_vehicles_involved_in_road_accidents,
    CAST("Number of Vehicles involved in accidents causing casualties" AS BIGINT) AS number_of_vehicles_involved_in_accidents_causing_casualties,
    CAST("Total Casualties" AS BIGINT) AS total_casualties,
    CAST("Number of  Fatal Casualties" AS BIGINT) AS number_of_fatal_casualties,
    CAST("Bus Operation statistics (BOS):  Number of Operational bus fleet (mid-year)" AS BIGINT) AS bus_operation_statistics_bos_number_of_operational_bus_fleet_mid_year,
    CAST("Bus Operation statistics (BOS):  Total vehicle - journeys (Thousand)" AS BIGINT) AS bus_operation_statistics_bos_total_vehicle_journeys_thousand,
    CAST("Bus Operation statistics (BOS):  Average vehicle -  journeys per day(Thousand)" AS DOUBLE) AS bus_operation_statistics_bos_average_vehicle_journeys_per_day_thousand,
    CAST("Bus Operation statistics (BOS): Total vehicle -  Kilometers(Thousand)" AS BIGINT) AS bus_operation_statistics_bos_total_vehicle_kilometers_thousand,
    CAST("Bus Operation statistics (BOS):  Averagel vehicle -  kilometers per day(Thousand)" AS BIGINT) AS bus_operation_statistics_bos_averagel_vehicle_kilometers_per_day_thousand,
    CAST("Bus Operation statistics (BOS):  Total gross receipts (Rs Mn)" AS BIGINT) AS bus_operation_statistics_bos_total_gross_receipts_rs_mn,
    CAST("Bus Operation statistics (BOS): : Average gross receipts per day (Rs Thousand)" AS BIGINT) AS bus_operation_statistics_bos_average_gross_receipts_per_day_rs_thousand,
    "__row_number" AS row_number,
    "__package_id" AS package_id,
    "__package_name" AS package_name,
    "__package_title" AS package_title,
    CAST("__package_metadata_modified" AS TIMESTAMP) AS package_metadata_modified,
    "__resource_id" AS resource_id,
    "__resource_name" AS resource_name,
    "__resource_format" AS resource_format,
    CAST("__resource_last_modified" AS TIMESTAMP) AS resource_last_modified
FROM "statistics-mauritius-transport-statistics-island-mauritius-2007-2016"
