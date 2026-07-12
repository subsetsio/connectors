-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "MEASURE: Measure" AS measure_measure,
    "FREQ: Frequency" AS freq_frequency,
    "PURPOSE: Purpose of stay" AS purpose_purpose_of_stay,
    "C_DEST: Country of destination" AS c_dest_country_of_destination,
    "TRA_MODE: Mode of transport" AS tra_mode_mode_of_transport,
    "DURATION: Length of stay" AS duration_length_of_stay,
    "ACCOMOD: Accommodation type" AS accomod_accommodation_type,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-dsd-tour-soc@df-c1706"
