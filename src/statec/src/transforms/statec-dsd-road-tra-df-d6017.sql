-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "MEASURE: Measure" AS measure_measure,
    "FREQ: Frequency" AS freq_frequency,
    "LOADSTAT: Loading status" AS loadstat_loading_status,
    "TRA_COV: Transport coverage" AS tra_cov_transport_coverage,
    "TRA_TYPE: Type of transport" AS tra_type_type_of_transport,
    "TRA_OPER: Type of operation and loading status" AS tra_oper_type_of_operation_and_loading_status,
    "NST07: Goods transported (NST 2007)" AS nst07_goods_transported_nst_2007,
    "C_ORIG: Country of origin" AS c_orig_country_of_origin,
    "C_DEST: Country of destination" AS c_dest_country_of_destination,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "COMMENT_DSET: Comments on the dataset levels" AS comment_dset_comments_on_the_dataset_levels,
    "COMMENT_OBS: Comments to the observation value" AS comment_obs_comments_to_the_observation_value,
    "COMMENT_TS_TRA_OPER: Detailed description of the group of series" AS comment_ts_tra_oper_detailed_description_of_the_group_of_series
FROM "statec-dsd-road-tra@df-d6017"
