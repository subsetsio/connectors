-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Some source dimensions or status fields are nullable in raw data; the declared grain uses only non-null dimensions.
-- caution: Raw table has duplicate rows across all non-null dimensions; no non-null raw row key is asserted for the pass-through table.
SELECT
    "GEO" AS geo,
    "SEX" AS sex,
    "FREQ" AS freq,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "DERA_MEASURE" AS dera_measure,
    "AGE" AS age,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-bts-sal-eqtp-sex-age"
