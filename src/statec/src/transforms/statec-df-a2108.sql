-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "MEASURE: Measure" AS measure_measure,
    "METEO_STATION: Meteo station" AS meteo_station_meteo_station,
    "NORME_CLIMAT: Climatological normals" AS norme_climat_climatological_normals,
    "MONTH: Month" AS month_month,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "COMMENT_DSET: Comments on the dataset levels" AS comment_dset_comments_on_the_dataset_levels,
    "COMMENT_OBS: Comments to the observation value" AS comment_obs_comments_to_the_observation_value,
    "COMMENT_TS: Detailed description of the group of series" AS comment_ts_detailed_description_of_the_group_of_series,
    "NOTE_NORME_CLIMAT: Note Climatological normals" AS note_norme_climat_note_climatological_normals,
    "NOTE_MESURE: Note Measure" AS note_mesure_note_measure,
    "NOTE_METEO_STATION: Note Meteo station" AS note_meteo_station_note_meteo_station
FROM "statec-df-a2108"
