SELECT
    identifier,
    name,
    unique_name,
    NULLIF(key_cricinfo, '')   AS key_cricinfo,
    NULLIF(key_cricinfo_2, '') AS key_cricinfo_2
FROM "cricsheet-people"
WHERE identifier IS NOT NULL AND identifier <> ''
