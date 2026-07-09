-- Personal income in Colorado, by area and year.
-- Dropped from the raw asset: period, periodtype, pertypdesc — all constant
-- (every row is an annual observation; folded into the column descriptions).
-- caution: mixes geographic levels (United States / State / MSA / County) in one column.
-- caution: `income_type` selects WHICH income measure `income` holds; rows of different types are not additive.
-- caution: `income_rank` is a rank, not a measure.
SELECT
    "stateabbrv"                            AS state_abbrev,
    "statename"                             AS state_name,
    CAST("stfips" AS BIGINT)                AS state_fips,
    CAST("areatype" AS BIGINT)              AS area_type,
    "areatyname"                            AS area_type_name,
    CAST("area" AS BIGINT)                  AS area_code,
    "areaname"                              AS area_name,
    CAST("periodyear" AS BIGINT)            AS period_year,
    CAST("inctype" AS BIGINT)               AS income_type,
    "incdesc"                               AS income_type_name,
    CAST("incsource" AS BIGINT)             AS income_source,
    "incsrcdesc"                            AS income_source_name,
    CAST("income" AS BIGINT)                AS income,
    CAST("incrank" AS BIGINT)               AS income_rank,
    CAST("population" AS BIGINT)            AS population,
    strptime("releasedate", '%Y%m%d')::DATE AS release_date
FROM "colorado-department-of-labor-and-employment-2cpa-vbur"
