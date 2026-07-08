SELECT
    CAST(record_id AS VARCHAR) AS record_id,
    identifier,
    title,
    country,
    category,
    subcategory,
    measure_type,
    status,
    date_type,
    sector_scope,
    social_partner_role,
    is_sector,
    is_occupation,
    CAST(try_strptime(NULLIF(start_date,  ''), '%m/%d/%Y') AS DATE) AS start_date,
    CAST(try_strptime(NULLIF(end_date,    ''), '%m/%d/%Y') AS DATE) AS end_date,
    CAST(try_strptime(NULLIF(last_update, ''), '%m/%d/%Y') AS DATE) AS last_update
FROM "eurofound-covid19-eu-policywatch"
WHERE record_id IS NOT NULL
