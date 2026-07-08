SELECT
    country, glacier_name,
    TRY_CAST(glacier_id AS BIGINT)         AS glacier_id,
    TRY_CAST(series_id AS BIGINT)          AS series_id,
    TRY_CAST(begin_date AS DATE)           AS begin_date,
    begin_date_unc,
    TRY_CAST(end_date AS DATE)             AS end_date,
    end_date_unc,
    TRY_CAST(length_change AS DOUBLE)      AS length_change,
    TRY_CAST(length_change_unc AS DOUBLE)  AS length_change_unc,
    length_change_direction,
    end_platform, end_method,
    investigators, agencies, "references" AS reference_ids, remarks
FROM "wgms-fog-front-variation"
