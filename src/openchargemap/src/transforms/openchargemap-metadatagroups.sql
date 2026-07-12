SELECT
    id,
    title,
    data_provider_id,
    is_restricted_edit,
    is_public_interest,
    metadata_fields_json,
    metadata_field_count
FROM "openchargemap-metadatagroups"
WHERE id IS NOT NULL
