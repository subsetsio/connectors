SELECT
    id,
    title,
    website_url,
    comments,
    contact_email,
    fault_report_email,
    phone_primary,
    phone_secondary,
    booking_url,
    is_private_individual,
    is_restricted_edit
FROM "openchargemap-operators"
WHERE id IS NOT NULL
