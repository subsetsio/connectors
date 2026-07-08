SELECT variable_name, income_type, mean_income, method,
       country_group, CAST(year AS INTEGER) AS year,
       CAST(gini AS DOUBLE) AS gini
FROM "bruegel-global-and-regional-gini-coefficients-income-inequality" WHERE gini IS NOT NULL
