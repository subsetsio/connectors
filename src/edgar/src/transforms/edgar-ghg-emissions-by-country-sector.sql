SELECT
    country_code,
    country_name,
    ipcc_annex,
    c_group,
    ipcc_sector_code,
    ipcc_sector_name,
    gas,
    fossil_bio,
    CAST(year AS INTEGER)        AS year,
    CAST(emissions_kt AS DOUBLE) AS emissions_kt
FROM "edgar-ghg-emissions-by-country-sector"
WHERE emissions_kt IS NOT NULL
  AND country_code IS NOT NULL
  AND gas IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY country_code, ipcc_sector_code, gas, fossil_bio, year
    ORDER BY emissions_kt DESC
) = 1
