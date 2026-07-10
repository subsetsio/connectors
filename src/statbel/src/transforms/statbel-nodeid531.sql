-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("DATE_DEATH", '%d/%m/%Y')::DATE AS date_death,
    CAST("CNT" AS BIGINT) AS cnt
FROM "statbel-nodeid531"
