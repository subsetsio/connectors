SELECT
    make_date(year, month, 1)        AS date,
    geo_type,
    geo_name,
    geo_code,
    index_nsa,
    index_sa
FROM "freddie-mac-house-price-index"
WHERE index_nsa IS NOT NULL
  AND index_sa IS NOT NULL
