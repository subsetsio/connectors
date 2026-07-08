SELECT
    CAST(year AS INTEGER) AS year,
    TRY_CAST(dry_bulk AS DOUBLE) AS dry_bulk,
    TRY_CAST(liquid_bulk AS DOUBLE) AS liquid_bulk,
    TRY_CAST(general_cargo AS DOUBLE) AS general_cargo,
    TRY_CAST(total AS DOUBLE) AS total
FROM "port-of-la-i9rh-q5gx"
WHERE year IS NOT NULL
