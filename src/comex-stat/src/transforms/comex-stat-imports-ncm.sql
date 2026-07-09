-- comex-stat-imports-ncm: monthly Brazilian trade at NCM (HS-8) detail, with the source's own codebooks joined in for labels

SELECT
    make_date(CAST(f."CO_ANO" AS BIGINT), CAST(f."CO_MES" AS BIGINT), 1) AS period,
    CAST(f."CO_ANO" AS BIGINT)                       AS year,
    CAST(f."CO_MES" AS BIGINT)                       AS month,
    f."CO_NCM"                                       AS ncm_code,
    TRIM(n."NO_NCM_ING")                             AS ncm_description_en,
    CAST(f."CO_UNID" AS BIGINT)                      AS unit_code,
    TRIM(u."NO_UNID")                                AS unit_name_pt,
    f."CO_PAIS"                                      AS country_code,
    p."CO_PAIS_ISOA3"                                AS country_iso_alpha3,
    p."NO_PAIS_ING"                                  AS country_name_en,
    f."SG_UF_NCM"                                    AS state_abbr,
    f."CO_VIA"                                       AS transport_mode_code,
    v."NO_VIA"                                       AS transport_mode_pt,
    f."CO_URF"                                       AS customs_unit_code,
    r."NO_URF"                                       AS customs_unit_pt,
    CAST(f."QT_ESTAT" AS BIGINT)                     AS statistical_quantity,
    CAST(f."KG_LIQUIDO" AS BIGINT)                   AS net_weight_kg,
    CAST(f."VL_FOB" AS BIGINT)                       AS fob_value_usd,
    CAST(f."VL_FRETE" AS BIGINT)                    AS freight_value_usd,
    CAST(f."VL_SEGURO" AS BIGINT)                   AS insurance_value_usd

FROM "comex-stat-imports-ncm" f
LEFT JOIN "comex-stat-ncm"          n ON f."CO_NCM"  = n."CO_NCM"
LEFT JOIN "comex-stat-ncm-unidade"  u ON f."CO_UNID" = u."CO_UNID"
LEFT JOIN "comex-stat-pais"         p ON f."CO_PAIS" = p."CO_PAIS"
LEFT JOIN "comex-stat-via"          v ON f."CO_VIA"  = v."CO_VIA"
LEFT JOIN "comex-stat-urf"          r ON f."CO_URF"  = r."CO_URF"
