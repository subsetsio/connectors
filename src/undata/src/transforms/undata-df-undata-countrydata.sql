-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: CountryData mixes countries, series, units, demographic breakdowns, and source types in one long table; filter the relevant dimensions before comparison or aggregation.
SELECT
    "DATAFLOW" AS dataflow,
    "FREQ" AS freq,
    "SERIES" AS series,
    "UNIT" AS unit,
    "LOCATION" AS location,
    "AGE_GROUP" AS age_group,
    "SEX" AS sex,
    "REF_AREA" AS ref_area,
    "SOURCE_TYPE" AS source_type,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    CAST("OBS_VALUE" AS DOUBLE) AS obs_value,
    CAST("UNIT_MULT" AS BIGINT) AS unit_mult,
    CAST("TIME_DETAIL" AS BIGINT) AS time_detail,
    "NATURE" AS nature,
    "SOURCE_DETAIL" AS source_detail,
    "FOOTNOTES" AS footnotes
FROM "undata-df-undata-countrydata"
