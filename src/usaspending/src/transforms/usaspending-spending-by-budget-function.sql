SELECT fiscal_year,
       code AS budget_function_code,
       name AS budget_function_name,
       total_obligations
FROM "usaspending-spending-by-budget-function"
WHERE total_obligations <> 0
