-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "UNIT_MEASURE: Unit of measure" AS unit_measure_unit_of_measure,
    "MEASURE: Measure" AS measure_measure,
    "FREQ: Frequency" AS freq_frequency,
    "AGE: Age" AS age_age,
    "SEX: Sex" AS sex_sex,
    "SEVERITY_INJ: Injury severity" AS severity_inj_injury_severity,
    "ROAD_USER_TYPE: Road user type" AS road_user_type_road_user_type,
    "ACCIDENT_TYPE: Collision type" AS accident_type_collision_type,
    "ROAD_SURFACE_CONDITION: Road surface conditon" AS road_surface_condition_road_surface_conditon,
    "ROAD_TYPE: Road type" AS road_type_road_type,
    "DAYSWEEK: Day of the week" AS daysweek_day_of_the_week,
    "GEO: Geographic level" AS geo_geographic_level,
    "SEVERITY_ACC: Accident severity" AS severity_acc_accident_severity,
    "TIME_PERIOD: Time period" AS time_period_time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT: Unit multiplier" AS unit_mult_unit_multiplier,
    "OBS_STATUS: Observation status" AS obs_status_observation_status,
    "DECIMALS: Decimals" AS decimals_decimals,
    "COMMENT_DSET: Comments on the dataset levels" AS comment_dset_comments_on_the_dataset_levels,
    "COMMENT_OBS: Comments to the observation value" AS comment_obs_comments_to_the_observation_value,
    "COMMENT_TS_ACCIDENT_TYPE: Detailed description of the group of series collision type" AS comment_ts_accident_type_detailed_description_of_the_group_of_series_collision_type,
    "COMMENT_TS_SEVERITY_ACC: Detailed description of the group of series accident severity" AS comment_ts_severity_acc_detailed_description_of_the_group_of_series_accident_severity,
    "COMMENT_TS_SEVERITY_INJ: Detailed description of the group of series inj severity" AS comment_ts_severity_inj_detailed_description_of_the_group_of_series_inj_severity
FROM "statec-dsd-accident@df-x040"
