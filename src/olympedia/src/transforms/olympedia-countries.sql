SELECT
    noc_code,
    country,
    CAST(competed_modern AS BOOLEAN) AS competed_modern,
    section
FROM "olympedia-countries"
WHERE noc_code IS NOT NULL AND country IS NOT NULL
