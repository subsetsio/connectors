SELECT
    last_day(make_date(year, month, 1))  AS date,
    currency_code,
    currency_name,
    units_per_usd,
    guaranies_per_unit
FROM "banco-central-del-paraguay-monthly-currency-reference-rates"
WHERE units_per_usd IS NOT NULL OR guaranies_per_unit IS NOT NULL
