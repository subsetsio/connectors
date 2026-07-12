-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "ACTIVITY: Economic activity (NACE Rev.2)" AS activity_economic_activity_nace_rev_2,
    "FREQ: Frequency" AS freq_frequency,
    "MEASURE: Measure" AS measure_measure,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_MEASURE: Note" AS note_measure_note,
    "DECIMALS: Decimals" AS decimals_decimals,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure
FROM "statec-df-c1204"
