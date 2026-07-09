SELECT
    iso_alpha3_code,
    country_or_area,
    NULLIF(NULLIF(region, '...'), '…')    AS region,
    NULLIF(NULLIF(subregion, '...'), '…') AS subregion
FROM "unodc-data-portal-wdr-regions"
WHERE iso_alpha3_code IS NOT NULL
