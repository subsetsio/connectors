-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Includes country, regional, and global SDG observations plus multiple demographic and custom breakdown dimensions; filter the relevant geography and breakdown columns before aggregating.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ" AS freq,
    "REPORTING_TYPE" AS reporting_type,
    "SERIES" AS series,
    CAST("REF_AREA" AS BIGINT) AS ref_area,
    "SEX" AS sex,
    "AGE" AS age,
    "URBANISATION" AS urbanisation,
    "INCOME_WEALTH_QUANTILE" AS income_wealth_quantile,
    "EDUCATION_LEV" AS education_lev,
    "OCCUPATION" AS occupation,
    "CUST_BREAKDOWN" AS cust_breakdown,
    "COMPOSITE_BREAKDOWN" AS composite_breakdown,
    "DISABILITY_STATUS" AS disability_status,
    "ACTIVITY" AS activity,
    "PRODUCT" AS product,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    "UNIT_MEASURE" AS unit_measure,
    "BASE_PER" AS base_per,
    "NATURE" AS nature,
    "TIME_DETAIL" AS time_detail,
    "COMMENT_OBS" AS comment_obs,
    "TIME_COVERAGE" AS time_coverage,
    "UPPER_BOUND" AS upper_bound,
    "LOWER_BOUND" AS lower_bound,
    "SOURCE_DETAIL" AS source_detail,
    "COMMENT_TS" AS comment_ts,
    "GEO_INFO_URL" AS geo_info_url,
    "GEO_INFO_TYPE" AS geo_info_type,
    "CUST_BREAKDOWN_LB" AS cust_breakdown_lb,
    "DATA_LAST_UPDATE" AS data_last_update
FROM "undata-df-sdg-glh"
