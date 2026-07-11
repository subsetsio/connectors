WITH normalized AS (
    SELECT DISTINCT
        strptime(CAST(month_date_yyyymm AS VARCHAR), '%Y%m')::DATE AS date,
        lpad(CAST(postal_code AS VARCHAR), 5, '0') AS postal_code,
        zip_name,

        CAST(median_listing_price AS DOUBLE)                  AS median_listing_price,
        CAST(active_listing_count AS BIGINT)                  AS active_listing_count,
        CAST(median_days_on_market AS BIGINT)                 AS median_days_on_market,
        CAST(new_listing_count AS BIGINT)                     AS new_listing_count,
        CAST(price_increased_count AS BIGINT)                 AS price_increased_count,
        CAST(price_increased_share AS DOUBLE)                 AS price_increased_share,
        CAST(price_reduced_count AS BIGINT)                   AS price_reduced_count,
        CAST(price_reduced_share AS DOUBLE)                   AS price_reduced_share,
        CAST(pending_listing_count AS BIGINT)                 AS pending_listing_count,
        CAST(median_listing_price_per_square_foot AS DOUBLE)  AS median_listing_price_per_square_foot,
        CAST(median_square_feet AS DOUBLE)                    AS median_square_feet,
        CAST(average_listing_price AS DOUBLE)                 AS average_listing_price,
        CAST(total_listing_count AS BIGINT)                   AS total_listing_count,
        CAST(pending_ratio AS DOUBLE)                         AS pending_ratio

    FROM "realtor-core-zip"
    WHERE postal_code IS NOT NULL
)
SELECT
    date,
    postal_code,
    row_number() OVER (
        PARTITION BY date, postal_code
        ORDER BY
            zip_name,
            median_listing_price,
            active_listing_count,
            median_days_on_market,
            new_listing_count,
            price_increased_count,
            price_increased_share,
            price_reduced_count,
            price_reduced_share,
            pending_listing_count,
            median_listing_price_per_square_foot,
            median_square_feet,
            average_listing_price,
            total_listing_count,
            pending_ratio
    ) AS zip_month_sequence,
    zip_name,
    median_listing_price,
    active_listing_count,
    median_days_on_market,
    new_listing_count,
    price_increased_count,
    price_increased_share,
    price_reduced_count,
    price_reduced_share,
    pending_listing_count,
    median_listing_price_per_square_foot,
    median_square_feet,
    average_listing_price,
    total_listing_count,
    pending_ratio
FROM normalized
