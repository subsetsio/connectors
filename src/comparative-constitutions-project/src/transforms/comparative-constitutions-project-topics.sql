SELECT
    key,
    label,
    description,
    count,
    keywords,
    to_json(topics) AS topics
FROM "comparative-constitutions-project-topics"
