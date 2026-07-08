SELECT
            CAST(CO_ANO AS INTEGER)        AS year,
            CAST(CO_MES AS INTEGER)        AS month,
            CO_NCM                         AS ncm_code,
            CO_UNID                        AS unit_code,
            CO_PAIS                        AS country_code,
            SG_UF_NCM                      AS state,
            CO_VIA                         AS transport_mode_code,
            CO_URF                         AS customs_code,
            TRY_CAST(QT_ESTAT AS BIGINT)   AS statistical_quantity,
            TRY_CAST(KG_LIQUIDO AS BIGINT) AS net_weight_kg,
            TRY_CAST(VL_FOB AS BIGINT)     AS fob_value_usd,
            TRY_CAST(VL_FRETE AS BIGINT)   AS freight_value_usd,
            TRY_CAST(VL_SEGURO AS BIGINT)  AS insurance_value_usd
FROM "comex-stat-imports-ncm"
WHERE CO_ANO IS NOT NULL
