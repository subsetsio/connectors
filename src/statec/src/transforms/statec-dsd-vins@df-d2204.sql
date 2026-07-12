-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "MEASURE: Measure" AS measure_measure,
    "FREQ: Frequency" AS freq_frequency,
    "C_DEST: Country of destination" AS c_dest_country_of_destination,
    "C_IMP: Country of origin" AS c_imp_country_of_origin,
    "AGREAREA: Agricultural area" AS agrearea_agricultural_area,
    "WINE_VAR: Main grape varieties" AS wine_var_main_grape_varieties,
    "PRINCIPAL_PRODUCT_TYPE: Main product types" AS principal_product_type_main_product_types,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "COMMENT_DSET: Comments on the dataset levels" AS comment_dset_comments_on_the_dataset_levels,
    "COMMENT_OBS: Comments to the observation value" AS comment_obs_comments_to_the_observation_value,
    "COMMENT_TS_WINE_VAR: Detailed description of the group of series wine" AS comment_ts_wine_var_detailed_description_of_the_group_of_series_wine,
    "REPYEARSTART: Reporting year start day" AS repyearstart_reporting_year_start_day,
    "COMMENT_TS_MEASURE: Detailed description of the group of series measure" AS comment_ts_measure_detailed_description_of_the_group_of_series_measure
FROM "statec-dsd-vins@df-d2204"
