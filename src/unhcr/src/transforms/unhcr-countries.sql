SELECT
    CAST(id AS BIGINT) AS country_id,
    code AS country_code,
    iso AS iso3,
    iso2,
    name,
    "nameOrigin" AS name_origin,
    "nameLong" AS name_long,
    "nameShort" AS name_short,
    "nameFormal" AS name_formal,
    nationality,
    "majorArea" AS major_area,
    region,
    "nameFr" AS name_fr,
    "majorAreaFr" AS major_area_fr,
    "regionFr" AS region_fr
FROM "unhcr-countries"
