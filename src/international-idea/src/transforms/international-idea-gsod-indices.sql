SELECT
    CAST(ID_country_code AS INTEGER)   AS country_code,
    ID_country_name                    AS country_name,
    CAST(ID_year AS INTEGER)           AS year,
    TRY_CAST(ID_region AS INTEGER)     AS region_id,
    TRY_CAST(ID_subregion AS INTEGER)  AS subregion_id,
    TRY_CAST(dem AS INTEGER)           AS dem_performance_band,
    TRY_CAST(demperf AS INTEGER)       AS dem_performance,
    TRY_CAST(COLUMNS('^(A|SA|SC)_') AS DOUBLE)
FROM "international-idea-gsod-indices"
WHERE ID_year IS NOT NULL AND ID_country_code IS NOT NULL
