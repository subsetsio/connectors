-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fips_county",
    "county_name",
    CAST("cases_asd" AS BIGINT) AS cases_asd,
    CAST("pop" AS BIGINT) AS pop,
    CAST("prevalence_asd" AS DOUBLE) AS prevalence_asd,
    "prevalence_asd_ci",
    "map_category"
FROM "cdc-7vg3-e5u2"
