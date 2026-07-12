-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "PARTNER: Partner" AS partner_partner,
    "COMPONENT: Component" AS component_component,
    "DIRECTION: Direction Flow" AS direction_direction_flow,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_PARTNER_2: Note Partner 2" AS note_partner_2_note_partner_2,
    "NOTE_PARTNER_1: Note Partner 1" AS note_partner_1_note_partner_1,
    "NOTE_COMPONENT_2: Note Component 2" AS note_component_2_note_component_2,
    "NOTE_COMPONENT_1: Note Component 1" AS note_component_1_note_component_1,
    "NOTE_DIRECTION_2: Note Direction Flow 2" AS note_direction_2_note_direction_flow_2,
    "NOTE_DIRECTION_1: Note Direction Flow 1" AS note_direction_1_note_direction_flow_1,
    "NOTE_YEAR_2: Note year 2" AS note_year_2_note_year_2,
    "NOTE_YEAR_1: Note year 1" AS note_year_1_note_year_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-e4211"
