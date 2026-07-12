-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "SPECIFICATION: Specification" AS specification_specification,
    "SURFACE_AREA: Surface Area" AS surface_area_surface_area,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_SPECIFICATION_2: Note specification 2" AS note_specification_2_note_specification_2,
    "NOTE_SPECIFICATION_1: Note specification 1" AS note_specification_1_note_specification_1,
    "NOTE_SURFACE_AREA_2: Note Surface Area 2" AS note_surface_area_2_note_surface_area_2,
    "NOTE_SURFACE_AREA_1: Note Surface Area 1" AS note_surface_area_1_note_surface_area_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-x010"
