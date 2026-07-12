-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "REF_AREA: Reference area" AS ref_area_reference_area,
    "FREQ: Frequency" AS freq_frequency,
    "MEASURE: Measure" AS measure_measure,
    "VEHICLE_TYPE: Vehicle type" AS vehicle_type_vehicle_type,
    "MOTOR_CAPACITY: Engine size (in cm3)" AS motor_capacity_engine_size_in_cm3,
    "BRAND: Brand" AS brand_brand,
    "MASS: Own weight (in kg)" AS mass_own_weight_in_kg,
    "MOTOR_ENERGY: Motor Energy" AS motor_energy_motor_energy,
    "AGE_CL: Age class (in years)" AS age_cl_age_class_in_years,
    "OPERATION: Operation type" AS operation_operation_type,
    "COLOR: Main color" AS color_main_color,
    "LENGTHREG: Length of registration period" AS lengthreg_length_of_registration_period,
    "TABLE_ID: Table Id" AS table_id_table_id,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    strptime("TIME_PERIOD: Time period", '%Y-%m')::DATE AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "DECIMALS: Decimal" AS decimals_decimal,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier
FROM "statec-df-d6134"
