SELECT valid_from, currency_code, country, currency_name, value
FROM (
    SELECT
        CAST(valid_from AS DATE) AS valid_from,
        currency_code,
        country,
        currency_name,
        CAST(value AS DOUBLE)    AS value,
        row_number() OVER (
            PARTITION BY valid_from, currency_code ORDER BY value DESC
        ) AS rn
    FROM "national-bank-of-slovakia-exchange-rate-foreign-monthly"
    WHERE value IS NOT NULL
)
WHERE rn = 1
