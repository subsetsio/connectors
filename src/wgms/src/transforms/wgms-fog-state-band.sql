SELECT
    country, glacier_name,
    TRY_CAST(glacier_id AS BIGINT)      AS glacier_id,
    TRY_CAST(state_id AS BIGINT)        AS state_id,
    TRY_CAST(lower_elevation AS DOUBLE) AS lower_elevation,
    TRY_CAST(upper_elevation AS DOUBLE) AS upper_elevation,
    TRY_CAST(mean_elevation AS DOUBLE)  AS mean_elevation,
    TRY_CAST(elevation_unc AS DOUBLE)   AS elevation_unc,
    TRY_CAST(area AS DOUBLE)            AS area,
    TRY_CAST(area_unc AS DOUBLE)        AS area_unc,
    remarks
FROM "wgms-fog-state-band"
