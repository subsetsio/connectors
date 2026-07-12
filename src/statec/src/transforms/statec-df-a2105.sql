-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ: Frequency" AS freq_frequency,
    "METEO_STATION: Meteo station" AS meteo_station_meteo_station,
    "YEARS: Year" AS years_year,
    "MONTH: Month" AS month_month,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "NOTE_METEO_STATION_2: Note station 2" AS note_meteo_station_2_note_station_2,
    "NOTE_METEO_STATION_1: Note station 1" AS note_meteo_station_1_note_station_1,
    "NOTE_YEAR_2: Note year 2" AS note_year_2_note_year_2,
    "NOTE_YEAR_1: Note year 1" AS note_year_1_note_year_1,
    "NOTE_MONTH_2: Note Month 2" AS note_month_2_note_month_2,
    "NOTE_MONTH_1: Note Month 1" AS note_month_1_note_month_1,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals
FROM "statec-df-a2105"
