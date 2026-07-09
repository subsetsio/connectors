-- Local Area Unemployment Statistics (LAUS) estimates for Colorado areas.
-- Dropped from the raw asset: stateabbrv, statename, stfips, benchmark — all constant.
-- caution: annual and monthly rows coexist (period_type); filter before aggregating over time.
-- caution: seasonally adjusted and unadjusted series overlap on every period (seasonally_adjusted).
-- caution: mixes State / MSA / County rows in one column.
SELECT
    CAST("areatype" AS BIGINT)   AS area_type,
    "areatyname"                 AS area_type_name,
    CAST("area" AS BIGINT)       AS area_code,
    "areaname"                   AS area_name,
    CAST("periodyear" AS BIGINT) AS period_year,
    CAST("periodtype" AS BIGINT) AS period_type,
    "pertypdesc"                 AS period_type_name,
    CAST("period" AS BIGINT)     AS period,
    CAST("adjusted" AS BOOLEAN)  AS seasonally_adjusted,
    CAST("prelim" AS BOOLEAN)    AS preliminary,
    CAST("laborforce" AS BIGINT) AS labor_force,
    CAST("emplab" AS BIGINT)     AS employed,
    CAST("unemp" AS BIGINT)      AS unemployed,
    CAST("unemprate" AS DOUBLE)  AS unemployment_rate
FROM "colorado-department-of-labor-and-employment-4e3w-qire"
