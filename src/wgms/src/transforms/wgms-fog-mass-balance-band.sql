SELECT
    country, glacier_name,
    TRY_CAST(glacier_id AS BIGINT)         AS glacier_id,
    TRY_CAST(year AS INTEGER)              AS year,
    TRY_CAST(lower_elevation AS DOUBLE)    AS lower_elevation,
    TRY_CAST(upper_elevation AS DOUBLE)    AS upper_elevation,
    TRY_CAST(area AS DOUBLE)               AS area,
    TRY_CAST(winter_balance AS DOUBLE)     AS winter_balance,
    TRY_CAST(winter_balance_unc AS DOUBLE) AS winter_balance_unc,
    TRY_CAST(summer_balance AS DOUBLE)     AS summer_balance,
    TRY_CAST(summer_balance_unc AS DOUBLE) AS summer_balance_unc,
    TRY_CAST(annual_balance AS DOUBLE)     AS annual_balance,
    TRY_CAST(annual_balance_unc AS DOUBLE) AS annual_balance_unc,
    remarks
FROM "wgms-fog-mass-balance-band"
