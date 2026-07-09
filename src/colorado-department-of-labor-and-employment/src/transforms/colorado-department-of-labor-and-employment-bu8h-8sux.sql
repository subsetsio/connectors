-- Population estimates by year for Colorado counties (a frozen 2015-vintage table).
-- Dropped from the raw asset: period, periodtype, pertypdesc (all rows annual) and
-- popsource/popsrcdesc (constant 'US Census Bureau Estimates') — folded into descriptions.
-- caution: mixes United States / State / County rows in one column.
SELECT
    "stateabbrv"                 AS state_abbrev,
    "statename"                  AS state_name,
    CAST("stfips" AS BIGINT)     AS state_fips,
    CAST("areatype" AS BIGINT)   AS area_type,
    "areatyname"                 AS area_type_name,
    CAST("area" AS BIGINT)       AS area_code,
    "areaname"                   AS area_name,
    CAST("periodyear" AS BIGINT) AS period_year,
    CAST("population" AS BIGINT) AS population
FROM "colorado-department-of-labor-and-employment-bu8h-8sux"
