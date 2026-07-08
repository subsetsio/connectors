SELECT
    CAST(year AS INTEGER)              AS year,
    month,
    CASE month WHEN 'jan' THEN 1 WHEN 'feb' THEN 2 WHEN 'mar' THEN 3 WHEN 'apr' THEN 4 WHEN 'may' THEN 5 WHEN 'jun' THEN 6 WHEN 'jul' THEN 7 WHEN 'aug' THEN 8 WHEN 'sep' THEN 9 WHEN 'oct' THEN 10 WHEN 'nov' THEN 11 WHEN 'dec' THEN 12 END                       AS month_num,
    st                                 AS state_fips,
    area                               AS area_code,
    industry_title,
    series,
    data_type,
    data_type_code,
    TRY_CAST(value AS DOUBLE)          AS employment_thousands
FROM (
    UNPIVOT "connecticut-department-of-labor-8zbs-9atu"
    ON jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec
    INTO NAME month VALUE value
)
WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
