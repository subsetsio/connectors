SELECT
    country, glacier_name,
    TRY_CAST(glacier_id AS BIGINT)           AS glacier_id,
    TRY_CAST(change_id AS BIGINT)            AS change_id,
    TRY_CAST(lower_elevation AS DOUBLE)      AS lower_elevation,
    TRY_CAST(upper_elevation AS DOUBLE)      AS upper_elevation,
    TRY_CAST(area AS DOUBLE)                 AS area,
    TRY_CAST(elevation_change AS DOUBLE)     AS elevation_change,
    TRY_CAST(elevation_change_unc AS DOUBLE) AS elevation_change_unc,
    TRY_CAST(volume_change AS DOUBLE)        AS volume_change,
    TRY_CAST(volume_change_unc AS DOUBLE)    AS volume_change_unc,
    remarks
FROM "wgms-fog-change-band"
