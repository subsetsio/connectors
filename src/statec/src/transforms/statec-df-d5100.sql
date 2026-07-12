-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "NACE_REV1_1: NACE REV 1.1" AS nace_rev1_1_nace_rev_1_1,
    "SPECIFICATION: Specification" AS specification_specification,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_YEARS_2: Note years 2" AS note_years_2_note_years_2,
    "NOTE_YEARS_1: Note years 1" AS note_years_1_note_years_1,
    "NOTE_NACE_REV1_1_2: Note NACE REV1.1" AS note_nace_rev1_1_2_note_nace_rev1_1,
    "NOTE_NACE_REV1_1_1: Note NACE REV1.1" AS note_nace_rev1_1_1_note_nace_rev1_1,
    "NOTE_SPECIFICATION_2: Note specification 2" AS note_specification_2_note_specification_2,
    "NOTE_SPECIFICATION_1: Note specification 1" AS note_specification_1_note_specification_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-d5100"
