-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Some source dimensions or status fields are nullable in raw data; the declared grain uses only non-null dimensions.
SELECT
    "GEO" AS geo,
    "NATIONALITY" AS nationality,
    "REU_LIST_TYPE" AS reu_list_type,
    "REU_REASON_REG" AS reu_reason_reg,
    "SEX" AS sex,
    "REU_REASON_RMV" AS reu_reason_rmv,
    "FREQ" AS freq,
    "TIME_PERIOD" AS time_period,
    "REU_ELECTION_TYPE" AS reu_election_type,
    "REU_MEASURE" AS reu_measure,
    "AGE" AS age,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-electoral"
