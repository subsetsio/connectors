SELECT
    id,
    title,
    formal_name,
    is_discontinued,
    is_obsolete
FROM "openchargemap-connectiontypes"
WHERE id IS NOT NULL
