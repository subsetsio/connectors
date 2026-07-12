SELECT fiscal_year,
       id AS budget_subfunction_id,
       code AS budget_subfunction_code,
       name AS budget_subfunction_name,
       total_obligations
FROM "usaspending-spending-by-budget-subfunction"
WHERE total_obligations <> 0
