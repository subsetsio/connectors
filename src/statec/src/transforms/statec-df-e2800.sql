-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "MEASURE: Measure" AS measure_measure,
    "OUTPUT: Output" AS output_output,
    "CULTURAL_DOMAIN: Cultural domain" AS cultural_domain_cultural_domain,
    "FREQ: Frequency" AS freq_frequency,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_MEASURE_2: Note Measure 2" AS note_measure_2_note_measure_2,
    "NOTE_MEASURE_1: Note Measure 1" AS note_measure_1_note_measure_1,
    "NOTE_YEAR_2: Note year 2" AS note_year_2_note_year_2,
    "NOTE_YEAR_1: Note year 1" AS note_year_1_note_year_1,
    "NOTE_OUTPUT_2: Note Output_2" AS note_output_2_note_output_2,
    "NOTE_OUTPUT_1: Note Output_1" AS note_output_1_note_output_1,
    "NOTE_CULTURAL_DOMAIN_2: Note Cultural domain 2" AS note_cultural_domain_2_note_cultural_domain_2,
    "NOTE_CULTURAL_DOMAIN_1: Note Cultural domain 1" AS note_cultural_domain_1_note_cultural_domain_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-e2800"
