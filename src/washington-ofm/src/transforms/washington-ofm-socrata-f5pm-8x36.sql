-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_entity_id" AS entity_id,
    "_source_type" AS source_type,
    "_socrata_dataset_id" AS socrata_dataset_id,
    "county_name",
    "county_fips_code",
    CAST("state_county_fips_code" AS BIGINT) AS state_county_fips_code,
    CAST("county_order_number" AS BIGINT) AS county_order_number,
    CAST("gnis_code" AS BIGINT) AS gnis_code,
    "gnis_tiger_format_code",
    CAST("geoid_tiger_code" AS BIGINT) AS geoid_tiger_code,
    "geoid_aff_code"
FROM "washington-ofm-socrata-f5pm-8x36"
