SELECT
    dataset_id,
    title,
    node_names,
    institutions,
    license,
    core,
    CAST(records AS BIGINT) AS records,
    CAST(occurrence_count AS BIGINT) AS occurrence_count,
    CAST(dropped_count AS BIGINT) AS dropped_count,
    TRY_CAST(published AS TIMESTAMP) AS published,
    TRY_CAST(created AS TIMESTAMP) AS created,
    TRY_CAST(updated AS TIMESTAMP) AS updated,
    extent_wkt,
    citation
FROM "obis-datasets"
WHERE dataset_id IS NOT NULL
