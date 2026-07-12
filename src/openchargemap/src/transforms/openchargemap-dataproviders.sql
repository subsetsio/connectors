SELECT
    id,
    title,
    website_url,
    comments,
    status_type_id,
    status_type_title,
    is_provider_enabled,
    is_restricted_edit,
    is_open_data_licensed,
    is_approved_import,
    license,
    date_last_imported
FROM "openchargemap-dataproviders"
WHERE id IS NOT NULL
