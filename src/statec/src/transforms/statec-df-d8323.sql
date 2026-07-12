-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "UNIT: Units" AS unit_units,
    "SIZECLASS: Size classes" AS sizeclass_size_classes,
    "INDICATOR: Innovation indicators" AS indicator_innovation_indicators,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "NOTE_PERIOD_2: Note 2 Years" AS note_period_2_note_2_years,
    "NOTE_PERIOD_1: Note 1 Years" AS note_period_1_note_1_years,
    "NOTE_UNIT_2: Note 2 Units" AS note_unit_2_note_2_units,
    "NOTE_UNIT_1: Note 1 Units" AS note_unit_1_note_1_units,
    "NOTE_SIZECLASS_2: Note 2 Size classes" AS note_sizeclass_2_note_2_size_classes,
    "NOTE_SIZECLASS_1: Note 1 Size classes" AS note_sizeclass_1_note_1_size_classes,
    "NOTE_INDICATOR_2: Note 2 Innovation indicators" AS note_indicator_2_note_2_innovation_indicators,
    "NOTE_INDICATOR_1: Note 1 Innovation indicators" AS note_indicator_1_note_1_innovation_indicators
FROM "statec-df-d8323"
