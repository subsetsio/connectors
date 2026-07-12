SELECT
    id,
    title,
    is_automated_checkin,
    is_positive
FROM "openchargemap-checkinstatustypes"
WHERE id IS NOT NULL
