-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "PARTY: Party" AS party_party,
    "MUNICIPALITY: Municipality" AS municipality_municipality,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_PARTY_2: Note Party 2" AS note_party_2_note_party_2,
    "NOTE_PARTY_1: Note Party 1" AS note_party_1_note_party_1,
    "NOTE_YEAR_2: Note year 2" AS note_year_2_note_year_2,
    "NOTE_YEAR_1: Note year 1" AS note_year_1_note_year_1,
    "NOTE_MUNICIPALITY_2: Note Municipality 2" AS note_municipality_2_note_municipality_2,
    "NOTE_MUNICIPALITY_1: Note Municipality 1" AS note_municipality_1_note_municipality_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-x053"
