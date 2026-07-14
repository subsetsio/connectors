-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PCS" AS pcs,
    "DECILE_NIVVIE" AS decile_nivvie,
    "SRCV_NB_DIFF" AS srcv_nb_diff,
    "SEX" AS sex,
    "SRCV_HLTH_SPH" AS srcv_hlth_sph,
    "SRCV_MEASURE" AS srcv_measure,
    "EDUC" AS educ,
    "TPH" AS tph,
    "GEO" AS geo,
    "NATIONALITY_TYPE" AS nationality_type,
    "EMPSTA_ENQ" AS empsta_enq,
    CAST("TIME_PERIOD" AS BIGINT) AS time_period,
    "AGE" AS age,
    "OBS_MEASURE" AS obs_measure,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-srcv-confiance"
