-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Multi-response crash factor file; rows are factor observations for a crash, not one row per crash.
SELECT
    CAST("STATE" AS BIGINT) AS state,
    "STATENAME" AS statename,
    CAST("ST_CASE" AS BIGINT) AS st_case,
    CAST("CRASHRF" AS BIGINT) AS crashrf,
    "CRASHRFNAME" AS crashrfname,
    "case_year"
FROM "nhtsa-fars-crashrf"
