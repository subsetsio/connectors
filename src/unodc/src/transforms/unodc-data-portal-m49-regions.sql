SELECT
    iso_alpha3_code,
    country_or_area,
    NULLIF(NULLIF(region, '...'), '…')    AS region,
    NULLIF(NULLIF(subregion, '...'), '…') AS subregion,
    NULLIF(NULLIF(intermediate_region, '...'), '…') AS intermediate_region
FROM "unodc-data-portal-m49-regions"
WHERE iso_alpha3_code IS NOT NULL
