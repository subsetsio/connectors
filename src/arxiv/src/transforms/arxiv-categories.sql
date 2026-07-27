-- arxiv-categories: arXiv subject taxonomy reference table.
-- Source: https://arxiv.org/category_taxonomy, fetched by src/nodes/arxiv.py.
SELECT
    category_id,
    category_name,
    group_name,
    archive_id,
    archive_name,
    description,
    source_url
FROM "arxiv-categories"
WHERE category_id IS NOT NULL
