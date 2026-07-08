SELECT bank_code, bank_name,
       CAST(base_rate AS DOUBLE)                   AS base_rate,
       CAST(base_lending_rate AS DOUBLE)           AS base_lending_rate,
       CAST(indicative_eff_lending_rate AS DOUBLE) AS indicative_eff_lending_rate,
       CAST(effective_date AS DATE)                AS effective_date
FROM "bank-negara-malaysia-base-rate"
WHERE bank_code IS NOT NULL
