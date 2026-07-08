SELECT CAST(date AS DATE) AS date,
       total_obligations,
       contract_obligations,
       direct_payment_obligations,
       grant_obligations,
       idv_obligations,
       loan_obligations,
       other_obligations
FROM "usaspending-monthly-spending-by-award-type"
WHERE total_obligations <> 0
