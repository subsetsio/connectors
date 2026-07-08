SELECT
    CAST(year AS INTEGER)                                          AS year,
    month,
    st                                                             AS state_fips,
    area                                                           AS area_code,
    publish_industry_title                                         AS industry_title,
    series,
    data_type,
    TRY_CAST(REPLACE(current_mo, ',', '') AS DOUBLE)              AS current_month_jobs,
    TRY_CAST(REPLACE(previous_mo, ',', '') AS DOUBLE)            AS previous_month_jobs,
    TRY_CAST(REPLACE(_1yr_ago_mo, ',', '') AS DOUBLE)            AS year_ago_jobs,
    TRY_CAST(REPLACE(diff_cur_prv, ',', '') AS DOUBLE)          AS change_from_previous,
    TRY_CAST(REPLACE(REPLACE(cur_prv, '%', ''), ',', '') AS DOUBLE)        AS pct_change_from_previous,
    TRY_CAST(REPLACE(diff_cur_1yr_ago, ',', '') AS DOUBLE)      AS change_from_year_ago,
    TRY_CAST(REPLACE(REPLACE(cur_1yr_ago, '%', ''), ',', '') AS DOUBLE)    AS pct_change_from_year_ago
FROM "connecticut-department-of-labor-h44w-mqs3"
