SELECT DISTINCT
    code AS currency_code,
    currency AS currency_name,
    CAST(in_table_a AS BOOLEAN) AS in_table_a,
    CAST(in_table_b AS BOOLEAN) AS in_table_b,
    CAST(in_table_c AS BOOLEAN) AS in_table_c
FROM "narodowy-bank-polski-currencies"
WHERE code IS NOT NULL
