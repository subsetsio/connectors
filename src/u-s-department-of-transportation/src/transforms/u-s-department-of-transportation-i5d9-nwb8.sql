-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "mode",
    CAST("dms_mode" AS BIGINT) AS dms_mode,
    CAST("tons2020" AS DOUBLE) AS tons2020,
    CAST("tons2021" AS DOUBLE) AS tons2021,
    CAST("tons2022" AS DOUBLE) AS tons2022,
    CAST("percent2020" AS DOUBLE) AS percent2020,
    CAST("percent2021" AS DOUBLE) AS percent2021,
    CAST("percent2022" AS DOUBLE) AS percent2022
FROM "u-s-department-of-transportation-i5d9-nwb8"
