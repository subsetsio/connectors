SELECT
    id,
    title,
    iso_code,
    continent_code
FROM "openchargemap-countries"
WHERE id IS NOT NULL
