SELECT
    country, glacier_name,
    TRY_CAST(glacier_id AS BIGINT) AS glacier_id,
    TRY_CAST(id AS BIGINT)         AS id,
    TRY_CAST(date AS DATE)         AS date,
    date_unc,
    TRY_CAST(latitude AS DOUBLE)   AS latitude,
    TRY_CAST(longitude AS DOUBLE)  AS longitude,
    description,
    surge, calving, flood, avalanche, rockfall, debris_flow,
    earthquake, volcanic_eruption, other,
    investigators, agencies, "references" AS reference_ids, remarks
FROM "wgms-fog-event"
