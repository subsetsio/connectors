SELECT
    transaction_id,
    CAST(price AS BIGINT)                        AS price,
    strptime(date_of_transfer, '%Y-%m-%d %H:%M')::DATE AS date_of_transfer,
    postcode,
    property_type,
    old_new,
    duration,
    paon, saon, street, locality, town_city, district, county,
    ppd_category_type,
    record_status
FROM "hm-land-registry-ppd"
WHERE price IS NOT NULL AND date_of_transfer IS NOT NULL
