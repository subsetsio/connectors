SELECT
    CAST(TagID AS BIGINT) AS tag_id,
    TagName AS tag_name,
    NULLIF(CAST(TagType AS VARCHAR), '') AS tag_type,
    TRY_CAST(NULLIF(CAST(TagOrder AS VARCHAR), '') AS INTEGER) AS tag_order
FROM "dhs-program-tags"
WHERE TagID IS NOT NULL
