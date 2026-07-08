SELECT
    metric,
    full_name,
    description,
    product,
    category,
    subcategory,
    unit,
    data_type,
    type,
    display_name,
    docs_url
FROM "coin-metrics-asset-metrics-catalog"
WHERE metric IS NOT NULL
