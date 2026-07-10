SELECT
    agreement_id,
    country,
    sector,
    CAST(nace_code AS VARCHAR) AS nace_code,
    description
FROM "eurofound-collectively-agreed-wages-nace"
WHERE agreement_id LIKE 'CA-%' AND nace_code IS NOT NULL
