-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Normals are climatological baseline summaries, not observations for the calculation date.
SELECT
    "feature_id",
    "STATION_NAME" AS station_name,
    "CLIMATE_IDENTIFIER" AS climate_identifier,
    "ID" AS id,
    "PERIOD" AS period,
    "CURRENT_FLAG" AS current_flag,
    "NORMAL_CODE" AS normal_code,
    "NORMAL_ID" AS normal_id,
    "PUBLICATION_CODE" AS publication_code,
    "DATE_CALCULATED" AS date_calculated,
    "FIRST_OCCURRENCE_DATE" AS first_occurrence_date,
    "PROVINCE_CODE" AS province_code,
    "PERIOD_BEGIN" AS period_begin,
    "PERIOD_END" AS period_end,
    "FIRST_YEAR" AS first_year,
    "FIRST_YEAR_NORMAL_PERIOD" AS first_year_normal_period,
    "LAST_YEAR" AS last_year,
    "LAST_YEAR_NORMAL_PERIOD" AS last_year_normal_period,
    "YEAR_COUNT_NORMAL_PERIOD" AS year_count_normal_period,
    "TOTAL_OBS_COUNT" AS total_obs_count,
    "OCCURRENCE_COUNT" AS occurrence_count,
    "MAX_DURATION_MISSING_YEARS" AS max_duration_missing_years,
    "PERCENT_OF_POSSIBLE_OBS" AS percent_of_possible_obs,
    "E_NORMAL_ELEMENT_NAME" AS e_normal_element_name,
    "F_NORMAL_ELEMENT_NAME" AS f_normal_element_name,
    "MONTH" AS month,
    "VALUE" AS value,
    "STN_ID" AS stn_id,
    "geometry_type",
    "longitude",
    "latitude"
FROM "environment-and-climate-change-canada-climate-normals"
