-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "UNIT: Units" AS unit_units,
    "INDICATOR: Innovation indicators" AS indicator_innovation_indicators,
    "NACE_REV2: NACE Rev.2" AS nace_rev2_nace_rev_2,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "NOTE_NACE_REV2_1: Note 1 NACE Rev.2" AS note_nace_rev2_1_note_1_nace_rev_2,
    "NOTE_PERIOD_2: Note 2 Years" AS note_period_2_note_2_years,
    "NOTE_PERIOD_1: Note 1 Years" AS note_period_1_note_1_years,
    "NOTE_UNIT_2: Note 2 Units" AS note_unit_2_note_2_units,
    "NOTE_UNIT_1: Note 1 Units" AS note_unit_1_note_1_units,
    "NOTE_NACE_REV2_2: Note 2 NACE Rev.2" AS note_nace_rev2_2_note_2_nace_rev_2,
    "NOTE_INDICATOR_2: Note 2 Innovation indicators" AS note_indicator_2_note_2_innovation_indicators,
    "NOTE_INDICATOR_1: Note 1 Innovation indicators" AS note_indicator_1_note_1_innovation_indicators
FROM "statec-df-d8322"
