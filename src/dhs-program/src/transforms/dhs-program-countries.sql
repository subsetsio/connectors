SELECT
    DHS_CountryCode AS country_code,
    CountryName AS country_name,
    NULLIF(CAST(ISO2_CountryCode AS VARCHAR), '') AS iso2_country_code,
    NULLIF(CAST(ISO3_CountryCode AS VARCHAR), '') AS iso3_country_code,
    NULLIF(CAST(FIPS_CountryCode AS VARCHAR), '') AS fips_country_code,
    NULLIF(CAST(UNSTAT_CountryCode AS VARCHAR), '') AS unstat_country_code,
    NULLIF(CAST(WHO_CountryCode AS VARCHAR), '') AS who_country_code,
    NULLIF(CAST(UNAIDS_CountryCode AS VARCHAR), '') AS unaids_country_code,
    NULLIF(CAST(UNICEF_CountryCode AS VARCHAR), '') AS unicef_country_code,
    NULLIF(CAST(RegionName AS VARCHAR), '') AS region_name,
    TRY_CAST(NULLIF(CAST(RegionOrder AS VARCHAR), '') AS INTEGER) AS region_order,
    NULLIF(CAST(SubregionName AS VARCHAR), '') AS subregion_name
FROM "dhs-program-countries"
WHERE DHS_CountryCode IS NOT NULL
