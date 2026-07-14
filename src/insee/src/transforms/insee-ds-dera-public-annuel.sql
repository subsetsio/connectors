-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Some source dimensions or status fields are nullable in raw data; the declared grain uses only non-null dimensions.
SELECT
    "GEO" AS geo,
    "QUANTILE" AS quantile,
    "SEX" AS sex,
    "CIVILSERVANT_STATUS" AS civilservant_status,
    "FREQ" AS freq,
    "PUBLIC_LEGAL_FORM" AS public_legal_form,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "UNIT_MEASURE" AS unit_measure,
    "WKTIME" AS wktime,
    "DERA_MEASURE" AS dera_measure,
    "PCS_ESE" AS pcs_ese,
    "AGE" AS age,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-dera-public-annuel"
