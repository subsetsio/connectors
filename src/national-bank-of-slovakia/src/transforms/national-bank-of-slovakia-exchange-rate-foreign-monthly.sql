SELECT
    CAST(valid_from    AS DATE)    AS valid_from,
    CAST(month_number  AS INTEGER) AS month_number,
    CAST(country       AS VARCHAR) AS country,
    CAST(currency_code AS VARCHAR) AS currency_code,
    CAST(currency_name AS VARCHAR) AS currency_name,
    CAST(value         AS DOUBLE)  AS value
FROM "national-bank-of-slovakia-exchange-rate-foreign-monthly"
WHERE value IS NOT NULL
