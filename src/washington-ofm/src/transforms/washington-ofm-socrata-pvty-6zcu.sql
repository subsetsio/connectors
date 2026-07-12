-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_entity_id" AS entity_id,
    "_source_type" AS source_type,
    "_socrata_dataset_id" AS socrata_dataset_id,
    CAST("block20l" AS BIGINT) AS block20l,
    CAST("state" AS BIGINT) AS state,
    "county",
    "countyname",
    "cityname",
    CAST("blkgrp20l" AS BIGINT) AS blkgrp20l,
    CAST("tract20l" AS BIGINT) AS tract20l,
    CAST("legdist22" AS BIGINT) AS legdist22,
    CAST("legdist24" AS BIGINT) AS legdist24,
    CAST("legdist24_pop_r" AS DOUBLE) AS legdist24_pop_r,
    CAST("legdist24_hu_r" AS DOUBLE) AS legdist24_hu_r,
    CAST("congdist22" AS BIGINT) AS congdist22,
    CAST("sduni" AS BIGINT) AS sduni,
    "sduniname",
    CAST("puma" AS BIGINT) AS puma,
    "pumaname",
    "vtd",
    CAST("zcta5" AS BIGINT) AS zcta5,
    "place",
    "placename",
    "placetype",
    CAST("uga" AS BIGINT) AS uga,
    "uganame"
FROM "washington-ofm-socrata-pvty-6zcu"
