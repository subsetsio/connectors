-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year_record" AS BIGINT) AS year_record,
    CAST("state_code" AS BIGINT) AS state_code,
    CAST("urban_code" AS BIGINT) AS urban_code,
    CAST("local_vmt" AS BIGINT) AS local_vmt,
    CAST("state_portion_pop" AS BIGINT) AS state_portion_pop,
    CAST("state_portion_land" AS BIGINT) AS state_portion_land
FROM "u-s-department-of-transportation-9wrh-mnib"
