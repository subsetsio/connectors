SELECT fiscal_year,
       id AS federal_account_id,
       account_number AS federal_account_number,
       name AS federal_account_name,
       total_obligations
FROM "usaspending-spending-by-federal-account"
WHERE total_obligations <> 0
