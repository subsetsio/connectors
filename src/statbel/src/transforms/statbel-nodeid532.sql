-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("DT_DATE", '%d/%m/%Y')::DATE AS dt_date,
    CAST("MS_NUM_BIRTHS" AS BIGINT) AS ms_num_births
FROM "statbel-nodeid532"
