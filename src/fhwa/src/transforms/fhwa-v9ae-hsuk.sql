SELECT
    CAST(route_id AS VARCHAR) AS route_id,
    CAST(natroute_id AS VARCHAR) AS natroute_id,
    CAST(state_code AS VARCHAR) AS state_code,
    CAST(year_record AS INTEGER) AS year_record,
    CAST(data_item AS VARCHAR) AS data_item,
    TRY_CAST(begin_point AS DOUBLE) AS begin_point,
    TRY_CAST(end_point AS DOUBLE) AS end_point,
    CAST(value_text AS VARCHAR) AS value_text,
    TRY_CAST(value_numeric AS DOUBLE) AS value_numeric,
    CAST(value_date AS VARCHAR) AS value_date
FROM "fhwa-v9ae-hsuk"
WHERE route_id IS NOT NULL
