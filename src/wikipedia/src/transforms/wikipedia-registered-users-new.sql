SELECT
    project,
    CAST(date AS DATE) AS date,
    "new_registered_users"
FROM "wikipedia-registered-users-new"
WHERE project IS NOT NULL
  AND date IS NOT NULL
  AND "new_registered_users" IS NOT NULL
