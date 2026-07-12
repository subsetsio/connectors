-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "ACT_LIGNE: Online activities" AS act_ligne_online_activities,
    "FREQ: Frequency" AS freq_frequency,
    "UNIT: Unit" AS unit_unit,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_ACT_LIGNE: Note" AS note_act_ligne_note,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-c1406"
