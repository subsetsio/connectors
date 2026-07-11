SELECT
    CAST(id AS INTEGER)    AS id,
    table_variable,
    CAST("order" AS INTEGER) AS code_order,
    short                  AS code_short,
    name                   AS code_name,
    wikipedia,
    description
FROM "parlgov-data-code"

