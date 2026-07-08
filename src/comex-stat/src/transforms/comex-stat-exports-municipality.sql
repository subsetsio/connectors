SELECT
            CAST(CO_ANO AS INTEGER)        AS year,
            CAST(CO_MES AS INTEGER)        AS month,
            SH4                            AS sh4_code,
            CO_PAIS                        AS country_code,
            SG_UF_MUN                      AS state,
            CO_MUN                         AS municipality_code,
            TRY_CAST(KG_LIQUIDO AS BIGINT) AS net_weight_kg,
            TRY_CAST(VL_FOB AS BIGINT)     AS fob_value_usd
FROM "comex-stat-exports-municipality"
WHERE CO_ANO IS NOT NULL
