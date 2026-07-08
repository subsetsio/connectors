SELECT
    TRY_CAST(year AS INTEGER)               AS year,
    TRY_CAST(area_km2 AS DOUBLE)            AS area_km2,
    TRY_CAST(mwe AS DOUBLE)                 AS mwe,
    TRY_CAST(mwe_sigma AS DOUBLE)           AS mwe_sigma,
    TRY_CAST(mwe_cumsum AS DOUBLE)          AS mwe_cumsum,
    TRY_CAST(gt AS DOUBLE)                  AS gt,
    TRY_CAST(gt_sigma AS DOUBLE)            AS gt_sigma,
    TRY_CAST(gt_cumsum AS DOUBLE)           AS gt_cumsum,
    TRY_CAST(gt_cumsum_sigma AS DOUBLE)     AS gt_cumsum_sigma,
    TRY_CAST(mmsle AS DOUBLE)               AS mmsle,
    TRY_CAST(mmsle_sigma AS DOUBLE)         AS mmsle_sigma,
    TRY_CAST(mmsle_cumsum AS DOUBLE)        AS mmsle_cumsum,
    TRY_CAST(mmsle_cumsum_sigma AS DOUBLE)  AS mmsle_cumsum_sigma
FROM "wgms-amce-global"
WHERE TRY_CAST(year AS INTEGER) IS NOT NULL
