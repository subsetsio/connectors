SELECT
    group_id,
    name,
    description,
    child_group_ids
FROM "sveriges-riksbank-groups"
WHERE group_id IS NOT NULL
