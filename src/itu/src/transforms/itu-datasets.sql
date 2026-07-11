SELECT
    dataset_id,
    dataset_short_name,
    dataset_type,
    team_short_name,
    team_name,
    email,
    publicly_visible,
    has_frozen_public_data
FROM "itu-datasets"
WHERE dataset_id IS NOT NULL
