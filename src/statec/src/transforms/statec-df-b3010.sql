-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ: Frequency" AS freq_frequency,
    "SPECIFICATION: Specification" AS specification_specification,
    strptime("TIME_PERIOD: Time period", '%Y-%m')::DATE AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_MONTH_2: Note Month 2" AS note_month_2_note_month_2,
    "NOTE_MONTH_1: Note Month 1" AS note_month_1_note_month_1,
    "NOTE_SPECIFICATION_2: Note specification 2" AS note_specification_2_note_specification_2,
    "NOTE_SPECIFICATION_1: Note specification 1" AS note_specification_1_note_specification_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-b3010"
