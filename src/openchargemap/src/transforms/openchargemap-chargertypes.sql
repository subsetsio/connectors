SELECT
    id,
    title,
    comments,
    is_fast_charge_capable
FROM "openchargemap-chargertypes"
WHERE id IS NOT NULL
