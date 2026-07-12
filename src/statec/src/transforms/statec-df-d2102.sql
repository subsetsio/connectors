-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ: Frequency" AS freq_frequency,
    "SURFACE_AREA: Surface Area" AS surface_area_surface_area,
    "SIZE_CLASS: Size class" AS size_class_size_class,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_YEAR_2: Note year 2" AS note_year_2_note_year_2,
    "NOTE_YEAR_1: Note year 1" AS note_year_1_note_year_1,
    "NOTE_SIZE_CLASS_2: Note Size class 2" AS note_size_class_2_note_size_class_2,
    "NOTE_SIZE_CLASS_1: Note Size class 1" AS note_size_class_1_note_size_class_1,
    "NOTE_SURFACE_AREA_2: Note Surface Area 2" AS note_surface_area_2_note_surface_area_2,
    "NOTE_SURFACE_AREA_1: Note Surface Area 1" AS note_surface_area_1_note_surface_area_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-d2102"
