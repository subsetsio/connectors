-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("ei_year" AS BIGINT) AS ei_year,
    CAST("dpm_tpy" AS BIGINT) AS dpm_tpy,
    CAST("nox_tpy" AS BIGINT) AS nox_tpy,
    CAST("sox_tpy" AS BIGINT) AS sox_tpy
FROM "port-of-la-2t3h-my34"
