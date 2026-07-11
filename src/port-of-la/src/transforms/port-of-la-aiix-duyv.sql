-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("date_name" AS BIGINT) AS date_name,
    CAST("nox_change_since_2005" AS DOUBLE) AS nox_change_since_2005,
    CAST("sox_change_since_2005" AS DOUBLE) AS sox_change_since_2005,
    CAST("dpm_change_since_2005" AS DOUBLE) AS dpm_change_since_2005
FROM "port-of-la-aiix-duyv"
