SELECT
    region,
    TRY_CAST(year AS INTEGER)      AS year,
    TRY_CAST(area_km2 AS DOUBLE)   AS area_km2,
    TRY_CAST(mwe AS DOUBLE)        AS mwe,
    TRY_CAST(mwe_sigma AS DOUBLE)  AS mwe_sigma,
    TRY_CAST(gt AS DOUBLE)         AS gt,
    TRY_CAST(gt_sigma AS DOUBLE)   AS gt_sigma
FROM "wgms-amce-region"
WHERE TRY_CAST(year AS INTEGER) IS NOT NULL
