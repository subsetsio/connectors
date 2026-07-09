-- Consumer Price Index series for the Denver CPI region and the United States
-- (a frozen 2014-vintage table).
-- Dropped from the raw asset: source / cpisourcedescription (constant, BLS) and
-- areadescription (an encyclopedia blurb about the area, not data).
-- caution: annual, monthly and semi-annual rows coexist; `period` is a month number
--          for monthly rows but a half-year end-month (6 or 12) for semi-annual rows.
-- caution: `series_type` selects the index series (CPI-U vs CPI-W, adjusted or not,
--          all-items vs expenditure category) — never aggregate across it.
SELECT
    CAST("statefips" AS BIGINT)         AS state_fips,
    CAST("areatype" AS BIGINT)          AS area_type,
    CAST("area" AS BIGINT)              AS area_code,
    "areaname"                          AS area_name,
    "dataregion"                        AS data_region,
    CAST("periodyear" AS BIGINT)        AS period_year,
    CAST("periodtype" AS BIGINT)        AS period_type,
    "periodtypedescription"             AS period_type_name,
    CAST("period" AS BIGINT)            AS period,
    CAST("type" AS BIGINT)              AS series_type,
    "title"                             AS series_title,
    CAST("cpi" AS DOUBLE)               AS cpi,
    CAST("percentchangeyear" AS DOUBLE) AS percent_change_year,
    CAST("percentchangemonth" AS DOUBLE) AS percent_change_month
FROM "colorado-department-of-labor-and-employment-bynd-i2hj"
