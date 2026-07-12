SELECT
    id,
    title,
    is_operational,
    is_user_selectable
FROM "openchargemap-statustypes"
WHERE id IS NOT NULL
