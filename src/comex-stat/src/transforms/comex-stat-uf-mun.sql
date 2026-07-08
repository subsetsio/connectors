SELECT
    CO_MUN_GEO AS municipality_code,
    NO_MUN     AS name,
    NO_MUN_MIN AS name_normalized,
    SG_UF      AS state
FROM "comex-stat-uf-mun"
WHERE CO_MUN_GEO IS NOT NULL
