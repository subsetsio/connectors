-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ: Frequency" AS freq_frequency,
    "SPECIAL_AGG: Special Aggregate NACE Rév.2" AS special_agg_special_aggregate_nace_r_v_2,
    "INDICATOR: Indicator" AS indicator_indicator,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "DECIMALS: Decimals" AS decimals_decimals,
    "NOTE_SPECIAL_AGG: Note to special aggregate" AS note_special_agg_note_to_special_aggregate,
    "NOTE_INDICATOR: Note to the indicator" AS note_indicator_note_to_the_indicator,
    "UNIT: Measurement unit" AS unit_measurement_unit,
    "OBS_STATUS: Observation status" AS obs_status_observation_status
FROM "statec-df-d1100"
