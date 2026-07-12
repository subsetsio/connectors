-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ: Frequency" AS freq_frequency,
    "SCHOOL: School" AS school_school,
    "CYCLE: Cycle" AS cycle_cycle,
    "SPECIFICATION: Specification" AS specification_specification,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_SCHOOL_2: Note School 2" AS note_school_2_note_school_2,
    "NOTE_SCHOOL_1: Note School 1" AS note_school_1_note_school_1,
    "NOTE_CYCLE_2: Note Cycle 2" AS note_cycle_2_note_cycle_2,
    "NOTE_CYCLE_1: Note Cycle 1" AS note_cycle_1_note_cycle_1,
    "NOTE_SPECIFICATION_2: Note specification 2" AS note_specification_2_note_specification_2,
    "NOTE_SPECIFICATION_1: Note specification 1" AS note_specification_1_note_specification_1,
    "NOTE_SCHOOL_YEAR_2: Note School Year 2" AS note_school_year_2_note_school_year_2,
    "NOTE_SCHOOL_YEAR_1: Note School Year 1" AS note_school_year_1_note_school_year_1,
    "REPYEARSTART: Reporting year start day" AS repyearstart_reporting_year_start_day,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-x046"
