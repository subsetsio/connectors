SELECT
    TEMCODIGO                         AS theme_code,
    TEMCODIGO_PAI                     AS parent_theme_code,
    TEMNOME                           AS theme_name
FROM "ipea-themes"
WHERE TEMCODIGO IS NOT NULL
