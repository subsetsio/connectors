-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year_record" AS BIGINT) AS year_record,
    CAST("state_code" AS BIGINT) AS state_code,
    CAST("rmc_vmt" AS BIGINT) AS rmc_vmt,
    CAST("rl_vmt" AS BIGINT) AS rl_vmt,
    CAST("su_vmt" AS BIGINT) AS su_vmt,
    CAST("rural_pop" AS BIGINT) AS rural_pop,
    CAST("rural_land_area" AS BIGINT) AS rural_land_area,
    CAST("su_pop" AS BIGINT) AS su_pop,
    CAST("su_land_area" AS BIGINT) AS su_land_area,
    CAST("paved_rmc_length" AS DOUBLE) AS paved_rmc_length,
    CAST("paved_rl_length" AS DOUBLE) AS paved_rl_length,
    CAST("paved_ul_length" AS DOUBLE) AS paved_ul_length,
    CAST("unpaved_rmc_length" AS DOUBLE) AS unpaved_rmc_length,
    CAST("unpaved_rl_length" AS DOUBLE) AS unpaved_rl_length,
    CAST("unpaved_ul_length" AS DOUBLE) AS unpaved_ul_length
FROM "u-s-department-of-transportation-x2p2-83w8"
