-- Current Employment Statistics (CES): employment, hours and earnings by industry
-- series for Colorado and its metropolitan areas.
-- Dropped from the raw asset: stateabbrv, statename, stfips (constant Colorado) and
-- supprecord, supppw, suppfem (constant flags carrying no information in this load).
-- caution: annual and monthly rows coexist (period_type); filter before aggregating.
-- caution: adjusted and unadjusted series, and several benchmark vintages, overlap.
-- caution: series_code is hierarchical (total nonfarm above supersectors above industries).
SELECT
    CAST("areatype" AS BIGINT)            AS area_type,
    "areatyname"                          AS area_type_name,
    CAST("area" AS BIGINT)                AS area_code,
    "areaname"                            AS area_name,
    CAST("periodyear" AS BIGINT)          AS period_year,
    CAST("periodtype" AS BIGINT)          AS period_type,
    "pertypdesc"                          AS period_type_name,
    CAST("period" AS BIGINT)              AS period,
    CAST("seriescode" AS BIGINT)          AS series_code,
    "seriesttls"                          AS series_title,
    "seriesdesc"                          AS naics_code,
    CAST("adjusted" AS BOOLEAN)           AS seasonally_adjusted,
    CAST("benchmark" AS BIGINT)           AS benchmark_year,
    CAST("prelim" AS BOOLEAN)             AS preliminary,
    CAST("empces" AS BIGINT)              AS employment,
    CAST("hours" AS DOUBLE)               AS production_worker_weekly_hours,
    CAST("earnings" AS DOUBLE)            AS production_worker_weekly_earnings,
    CAST("hourearn" AS DOUBLE)            AS production_worker_hourly_earnings,
    CAST("hoursallwrkr" AS DOUBLE)        AS all_worker_weekly_hours,
    CAST("earningsallwrkr" AS DOUBLE)     AS all_worker_weekly_earnings,
    CAST("hourearnallwrkr" AS DOUBLE)     AS all_worker_hourly_earnings,
    CAST("supphe" AS BOOLEAN)             AS production_worker_hours_earnings_suppressed,
    CAST("suppheallwrkr" AS BOOLEAN)      AS all_worker_hours_earnings_suppressed
FROM "colorado-department-of-labor-and-employment-pt2g-89wc"
