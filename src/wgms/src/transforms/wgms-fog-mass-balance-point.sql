SELECT
    country, glacier_name,
    TRY_CAST(glacier_id AS BIGINT)   AS glacier_id,
    TRY_CAST(year AS INTEGER)        AS year,
    TRY_CAST(id AS BIGINT)           AS id,
    original_id, time_system,
    TRY_CAST(begin_date AS DATE)     AS begin_date,
    begin_date_unc,
    TRY_CAST(end_date AS DATE)       AS end_date,
    end_date_unc,
    TRY_CAST(latitude AS DOUBLE)     AS latitude,
    TRY_CAST(longitude AS DOUBLE)    AS longitude,
    TRY_CAST(elevation AS DOUBLE)    AS elevation,
    TRY_CAST(balance AS DOUBLE)      AS balance,
    TRY_CAST(balance_unc AS DOUBLE)  AS balance_unc,
    TRY_CAST(density AS DOUBLE)      AS density,
    TRY_CAST(density_unc AS DOUBLE)  AS density_unc,
    method, balance_code, remarks
FROM "wgms-fog-mass-balance-point"
