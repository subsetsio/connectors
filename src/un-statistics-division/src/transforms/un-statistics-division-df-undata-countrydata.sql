-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains multiple UNdata series, units, age groups, sexes, source types, and reference areas; filter to a coherent slice before comparing or aggregating observations.
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
    "TIME_PERIOD" AS time_period,
    "OBS_VALUE" AS obs_value,
    "UNIT_MULT" AS unit_mult,
    "TIME_DETAIL" AS time_detail,
    "NATURE" AS nature,
    "SOURCE_DETAIL" AS source_detail,
    "FOOTNOTES" AS footnotes
FROM "un-statistics-division-df-undata-countrydata"
