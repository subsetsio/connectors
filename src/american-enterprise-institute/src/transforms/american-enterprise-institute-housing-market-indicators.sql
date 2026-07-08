SELECT
    metro,
    metro_group,
    year_quarter,
    CAST(split_part(year_quarter, ':', 1) AS INTEGER) AS year,
    CAST(replace(split_part(year_quarter, ':', 2), 'Q', '') AS INTEGER) AS quarter,
    segment,
    segment_share_of_sales,
    median_sale_price,
    stressed_mortgage_default_rate,
    months_supply,
    new_construction_share_of_sales,
    new_construction_contribution_existing_stock,
    hpa_yoy,
    hpa_qoq,
    cumulative_hpa_since_2012
FROM "american-enterprise-institute-housing-market-indicators"
WHERE metro IS NOT NULL
  AND year_quarter IS NOT NULL
  AND regexp_matches(year_quarter, '^[0-9]{4}:Q[1-4]$')
