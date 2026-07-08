SELECT
    region,
    outline_id,
    TRY_CAST(glacier_id AS BIGINT) AS glacier_id,
    TRY_CAST(latitude AS DOUBLE)   AS latitude,
    TRY_CAST(longitude AS DOUBLE)  AS longitude,
    TRY_CAST(area_km2 AS DOUBLE)   AS area_km2,
    TRY_CAST(year AS INTEGER)      AS year,
    TRY_CAST(mwe AS DOUBLE)        AS mwe
FROM "wgms-amce-glacier"
WHERE TRY_CAST(year AS INTEGER) IS NOT NULL
  AND mwe IS NOT NULL
