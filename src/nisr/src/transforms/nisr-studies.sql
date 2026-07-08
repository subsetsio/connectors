SELECT
    TRY_CAST(id AS BIGINT)      AS study_id,
    surveyid,
    titl                        AS title,
    nation,
    authenty                    AS authority,
    NULLIF(data_coll_start, '0') AS data_collection_start,
    NULLIF(data_coll_end, '0')   AS data_collection_end,
    created                     AS created,
    changed                     AS changed
FROM "nisr-studies"
WHERE id IS NOT NULL AND TRIM(id) <> ''
QUALIFY row_number() OVER (PARTITION BY id ORDER BY changed DESC) = 1
