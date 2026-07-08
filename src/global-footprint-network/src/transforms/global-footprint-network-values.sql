SELECT
    CAST(year AS INTEGER)          AS year,
    CAST(countryCode AS BIGINT)    AS country_code,
    countryName                    AS country_name,
    shortName                      AS short_name,
    isoa2                          AS iso_a2,
    record                         AS record_type,
    CAST(value AS DOUBLE)          AS value,
    score                          AS data_quality_score,
    CAST(cropLand AS DOUBLE)       AS crop_land,
    CAST(grazingLand AS DOUBLE)    AS grazing_land,
    CAST(forestLand AS DOUBLE)     AS forest_land,
    CAST(fishingGround AS DOUBLE)  AS fishing_ground,
    CAST(builtupLand AS DOUBLE)    AS builtup_land,
    CAST(carbon AS DOUBLE)         AS carbon
FROM "global-footprint-network-values"
WHERE value IS NOT NULL
