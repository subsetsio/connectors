SELECT
    country,
    short_name,
    names,
    TRY_CAST(id AS BIGINT)                AS glacier_id,
    TRY_CAST(latitude AS DOUBLE)          AS latitude,
    TRY_CAST(longitude AS DOUBLE)         AS longitude,
    gtng_region,
    glims_id, rgi50_ids, rgi60_ids, rgi70_ids, wgi_id,
    TRY_CAST(parent_glacier_id AS BIGINT) AS parent_glacier_id,
    "references"                          AS reference_ids,
    remarks
FROM "wgms-fog-glacier"
