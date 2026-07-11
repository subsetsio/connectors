SELECT
    NIVNOME                           AS geo_level,
    TERCODIGO                         AS territory_code,
    TERNOME                           AS territory_name,
    TERNOMEPADRAO                     AS normalized_name,
    TERCAPITAL                        AS is_capital,
    TERAREA                           AS area,
    NIVAMC                            AS is_amc_level
FROM "ipea-territories"
WHERE TERCODIGO IS NOT NULL
