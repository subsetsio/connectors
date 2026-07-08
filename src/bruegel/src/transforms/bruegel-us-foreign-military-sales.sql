SELECT
    TRY_CAST(id AS INTEGER)               AS id,
    country,
    TRY_CAST(financial_value AS DOUBLE)   AS financial_value_bn_usd,
    main_equipment,
    military_domain,
    general_item_type,
    specific_item_type,
    contractors,
    TRY_CAST(year AS INTEGER)             AS year,
    TRY_CAST(month AS INTEGER)            AS month
FROM "bruegel-us-foreign-military-sales" WHERE country IS NOT NULL
