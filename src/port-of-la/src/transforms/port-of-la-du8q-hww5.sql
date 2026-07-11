SELECT
    fiscal_year,
    account_name,
    TRY_CAST(appropriation_amount AS DOUBLE) AS appropriation_amount,
    expense_categories
FROM "port-of-la-du8q-hww5"
WHERE fiscal_year IS NOT NULL OR account_name IS NOT NULL
