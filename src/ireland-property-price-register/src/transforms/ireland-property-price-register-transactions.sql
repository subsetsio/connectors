SELECT
    strptime(date_of_sale, '%d/%m/%Y')::DATE                 AS sale_date,
    file_year                                                AS year,
    trim(county)                                             AS county,
    nullif(trim(eircode), '')                                AS eircode,
    trim(address)                                            AS address,
    CAST(regexp_replace(price, '[^0-9.]', '', 'g') AS DOUBLE) AS price_eur,
    (not_full_market_price = 'Yes')                          AS not_full_market_price,
    (vat_exclusive = 'Yes')                                  AS vat_exclusive,
    description_of_property                                  AS description,
    nullif(trim(property_size_description), '')              AS property_size_description
FROM "ireland-property-price-register-transactions"
WHERE date_of_sale IS NOT NULL AND date_of_sale <> ''
