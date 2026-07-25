-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("vessel_id" AS BIGINT) AS vessel_id,
    CAST("operator_id" AS BIGINT) AS operator_id,
    "vessel_name",
    "uscg_number",
    CAST("in_service" AS BOOLEAN) AS in_service,
    CAST("carries_passengers" AS BOOLEAN) AS carries_passengers,
    CAST("carries_vehicles" AS BOOLEAN) AS carries_vehicles,
    CAST("carries_freight" AS BOOLEAN) AS carries_freight,
    CAST("passenger_capacity" AS BIGINT) AS passenger_capacity,
    CAST("vehicle_capacity" AS BIGINT) AS vehicle_capacity,
    "fuel_type",
    "fuel_other",
    CAST("typical_speed" AS BIGINT) AS typical_speed,
    CAST("year_built" AS BIGINT) AS year_built,
    CAST("main_horsepower_ahead" AS BIGINT) AS main_horsepower_ahead,
    CAST("main_horsepower_astern" AS BIGINT) AS main_horsepower_astern,
    "hull_material",
    "hull_shape",
    "propulsion_type",
    CAST("self_prop_indicator" AS BOOLEAN) AS self_prop_indicator,
    CAST("registered_breadth" AS DOUBLE) AS registered_breadth,
    CAST("registered_depth" AS DOUBLE) AS registered_depth,
    CAST("registered_length" AS DOUBLE) AS registered_length,
    CAST("registered_net_tons" AS BIGINT) AS registered_net_tons,
    CAST("registered_gross_tons" AS BIGINT) AS registered_gross_tons,
    "vessel_ownership",
    "vessel_owned_by",
    "vessel_operation",
    "vessel_operated_by",
    CAST("fuel_mileage" AS DOUBLE) AS fuel_mileage,
    CAST("ada_accessible" AS BOOLEAN) AS ada_accessible,
    CAST("expected_lifespan" AS BIGINT) AS expected_lifespan,
    "vessel_type",
    CAST("census_year_miles" AS BIGINT) AS census_year_miles,
    CAST("census_year" AS BIGINT) AS census_year,
    CAST("data_year" AS BIGINT) AS data_year
FROM "u-s-department-of-transportation-xkuc-f3hj"
