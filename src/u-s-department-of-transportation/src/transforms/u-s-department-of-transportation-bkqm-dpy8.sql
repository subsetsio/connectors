-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year_record" AS BIGINT) AS year_record,
    CAST("state_code" AS BIGINT) AS state_code,
    CAST("county_code" AS BIGINT) AS county_code,
    CAST("f_system" AS BIGINT) AS f_system,
    CAST("urban_code" AS BIGINT) AS urban_code,
    CAST("ownership" AS BIGINT) AS ownership,
    CAST("rmc_l_system_length" AS DOUBLE) AS rmc_l_system_length
FROM "u-s-department-of-transportation-bkqm-dpy8"
