SELECT
    id,
    title,
    is_pay_at_location,
    is_membership_required,
    is_access_key_required
FROM "openchargemap-usagetypes"
WHERE id IS NOT NULL
