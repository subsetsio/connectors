-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_entity_id" AS entity_id,
    "_source_type" AS source_type,
    "_socrata_dataset_id" AS socrata_dataset_id,
    "congressional_district",
    CAST("total_population_2010" AS BIGINT) AS total_population_2010,
    CAST("population_density_persons_square_mile_2010" AS DOUBLE) AS population_density_persons_square_mile_2010,
    CAST("total_housing_units_2010" AS BIGINT) AS total_housing_units_2010,
    CAST("occupied_housing_units_2010" AS BIGINT) AS occupied_housing_units_2010,
    CAST("vacant_housing_units_2010" AS BIGINT) AS vacant_housing_units_2010,
    CAST("occupancy_rate_2010" AS DOUBLE) AS occupancy_rate_2010,
    CAST("vacancy_rate_2010" AS DOUBLE) AS vacancy_rate_2010,
    CAST("land_area_square_miles_2010" AS DOUBLE) AS land_area_square_miles_2010,
    CAST("total_area_square_miles_2010" AS DOUBLE) AS total_area_square_miles_2010,
    CAST("water_area_2010" AS DOUBLE) AS water_area_2010
FROM "washington-ofm-socrata-um6h-4brj"
