SELECT
    id                          AS indicator_code,
    name                        AS indicator_name,
    description,
    section                     AS parent_code,
    color,
    selectable,
    TRY_CAST("Weight" AS DOUBLE) AS weight
FROM "international-idea-gsod-indicators"
WHERE id IS NOT NULL
