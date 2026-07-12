-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ: Frequency" AS freq_frequency,
    "DIRECTION: Direction Flow" AS direction_direction_flow,
    "COMPONENT: Component" AS component_component,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_DIRECTION_2: Note Direction Flow 2" AS note_direction_2_note_direction_flow_2,
    "NOTE_DIRECTION_1: Note Direction Flow 1" AS note_direction_1_note_direction_flow_1,
    "NOTE_COMPONENT_2: Note Component 2" AS note_component_2_note_component_2,
    "NOTE_COMPONENT_1: Note Component 1" AS note_component_1_note_component_1,
    "NOTE_QUARTER_2: Note quarter 2" AS note_quarter_2_note_quarter_2,
    "NOTE_QUARTER_1: Note quarter 1" AS note_quarter_1_note_quarter_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-e4202"
