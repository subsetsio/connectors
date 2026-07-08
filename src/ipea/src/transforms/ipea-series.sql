SELECT
    SERCODIGO                              AS series_code,
    SERNOME                                AS name,
    SERCOMENTARIO                          AS description,
    BASNOME                                AS database,
    TEMCODIGO                              AS theme_code,
    FNTSIGLA                               AS source_acronym,
    FNTNOME                                AS source_name,
    NULLIF(FNTURL, '')                     AS source_url,
    PERNOME                                AS periodicity,
    UNINOME                                AS unit,
    NULLIF(MULNOME, '')                    AS multiplier,
    SERSTATUS                              AS status,
    PAICODIGO                              AS country_code,
    SERNUMERICA                            AS is_numeric,
    CAST(SERATUALIZACAO AS TIMESTAMP)      AS last_updated
FROM "ipea-series"
WHERE SERCODIGO IS NOT NULL
