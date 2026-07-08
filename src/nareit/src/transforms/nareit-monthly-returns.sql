SELECT
    date,
    "index",
    "group",
    total_return,
    total_index,
    price_return,
    price_index,
    income_return,
    dividend_yield
FROM "nareit-monthly-returns"
WHERE total_return IS NOT NULL
ORDER BY "index", date
