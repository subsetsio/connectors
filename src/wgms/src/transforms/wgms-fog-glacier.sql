-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    "short_name",
    "names",
    CAST("id" AS BIGINT) AS id,
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    "gtng_region",
    "glims_id",
    "rgi50_ids",
    "rgi60_ids",
    "rgi70_ids",
    "wgi_id",
    CAST("parent_glacier_id" AS BIGINT) AS parent_glacier_id,
    "references",
    "remarks"
FROM "wgms-fog-glacier"
