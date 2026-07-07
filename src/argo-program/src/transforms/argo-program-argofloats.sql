SELECT
    CAST(dataset_id AS VARCHAR) AS dataset_id,
    CAST(row_type AS VARCHAR) AS row_type,
    CAST(variable_name AS VARCHAR) AS variable_name,
    CAST(COALESCE(attribute_name, '__variable__') AS VARCHAR) AS attribute_name,
    CAST(data_type AS VARCHAR) AS data_type,
    CAST(value AS VARCHAR) AS value,
    CAST(source_url AS VARCHAR) AS source_url
FROM "argo-program-argofloats"
WHERE dataset_id IS NOT NULL
  AND row_type IS NOT NULL
  AND variable_name IS NOT NULL
