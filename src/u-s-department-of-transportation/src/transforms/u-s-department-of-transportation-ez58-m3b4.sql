-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "origin_county_fips",
    "orig_state",
    "orig_county_name",
    "dest_county_fips",
    "dest_state",
    "dest_county_name",
    CAST("year" AS BIGINT) AS year,
    "pair_moves",
    CAST("tt_percentile_25" AS DOUBLE) AS tt_percentile_25,
    CAST("tt_percentile_50" AS DOUBLE) AS tt_percentile_50,
    CAST("tt_percentile_75" AS DOUBLE) AS tt_percentile_75
FROM "u-s-department-of-transportation-ez58-m3b4"
