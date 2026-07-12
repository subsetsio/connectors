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
    "city_name",
    "city_fips_code",
    "city_fips_code_90",
    CAST("gnis_code" AS BIGINT) AS gnis_code,
    "gnis_tiger_format_code",
    "place_name",
    "multi_county_flag"
FROM "washington-ofm-socrata-g2kf-7usg"
