-- comex-stat-uf-mun: reference/codebook table — trimmed labels, typed codes
SELECT
    CAST("CO_MUN_GEO" AS BIGINT) AS municipality_code,
    TRIM("NO_MUN")               AS name_pt,
    TRIM("NO_MUN_MIN")           AS name_pt_lower,
    TRIM("SG_UF")                AS state_abbr
FROM "comex-stat-uf-mun"
