-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Census tables can include geographic aggregates and categorical totals together with detailed categories; filter geography and category dimensions before summing observations.
-- caution: Raw extract contains repeated variable/modality rows and no non-null row key is asserted for the pass-through table.
SELECT
    "COD_VAR" AS cod_var,
    "LIB_VAR" AS lib_var,
    "COD_MOD" AS cod_mod,
    "LIB_MOD" AS lib_mod,
    "OBS_VALUE" AS obs_value,
    "OBS_MEASURE" AS obs_measure,
    "OBS_STATUS" AS obs_status
FROM "insee-ds-rp-education"
