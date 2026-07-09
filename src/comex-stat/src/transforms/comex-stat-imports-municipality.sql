-- comex-stat-imports-municipality: monthly Brazilian trade at importer-municipality and HS-4 detail, with country/municipality/product labels joined in

SELECT
    make_date(CAST(f."CO_ANO" AS BIGINT), CAST(f."CO_MES" AS BIGINT), 1) AS period,
    CAST(f."CO_ANO" AS BIGINT)                       AS year,
    CAST(f."CO_MES" AS BIGINT)                       AS month,
    f."SH4"                                          AS sh4_code,
    s.sh4_description_en                             AS sh4_description_en,
    f."CO_PAIS"                                      AS country_code,
    p."CO_PAIS_ISOA3"                                AS country_iso_alpha3,
    p."NO_PAIS_ING"                                  AS country_name_en,
    f."SG_UF_MUN"                                    AS state_abbr,
    CAST(f."CO_MUN" AS BIGINT)                       AS municipality_code,
    m."NO_MUN"                                       AS municipality_name,
    CAST(f."KG_LIQUIDO" AS BIGINT)                   AS net_weight_kg,
    CAST(f."VL_FOB" AS BIGINT)                       AS fob_value_usd
FROM "comex-stat-imports-municipality" f
LEFT JOIN (
    SELECT "CO_SH4" AS sh4_code, any_value(TRIM("NO_SH4_ING")) AS sh4_description_en
    FROM "comex-stat-ncm-sh" GROUP BY 1
) s ON f."SH4" = s.sh4_code
LEFT JOIN "comex-stat-pais" p ON f."CO_PAIS" = p."CO_PAIS"
LEFT JOIN "comex-stat-uf-mun" m ON CAST(f."CO_MUN" AS BIGINT) = CAST(m."CO_MUN_GEO" AS BIGINT)
