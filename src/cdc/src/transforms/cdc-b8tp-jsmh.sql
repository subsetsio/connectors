-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "TAXON" AS taxon,
    CAST("IS_OAW" AS BOOLEAN) AS is_oaw,
    CAST("IS_SUBTREE" AS BOOLEAN) AS is_subtree,
    CAST("N450_MATCHES_WGS" AS BOOLEAN) AS n450_matches_wgs,
    CAST("N450_EXISTS" AS BOOLEAN) AS n450_exists,
    CAST("WGS_EXISTS" AS BOOLEAN) AS wgs_exists,
    "WHO_NAME" AS who_name,
    "N450_GENBANK_ACCESSION" AS n450_genbank_accession,
    "WGS_GENBANK_ACCESSION" AS wgs_genbank_accession,
    "BIOSAMPLE" AS biosample,
    "COUNTRY" AS country,
    CAST("EPI_WEEK" AS BIGINT) AS epi_week,
    CAST("YEAR" AS BIGINT) AS year,
    CAST("CASE_NUMBER" AS BIGINT) AS case_number,
    "FLIGHT" AS flight,
    "FLIGHTS_WITH_MULTIPLE_WGS" AS flights_with_multiple_wgs,
    "BARRACK_BAY_MULTIPLE" AS barrack_bay_multiple,
    "RASH_ONSET" AS rash_onset,
    "BASE" AS base,
    CAST("CLUSTER" AS BIGINT) AS cluster,
    CAST("FAMILY_GROUP" AS BIGINT) AS family_group,
    "SUBCLUSTER" AS subcluster,
    CAST("BASE_FACTOR" AS BIGINT) AS base_factor,
    "IMPORT" AS import
FROM "cdc-b8tp-jsmh"
