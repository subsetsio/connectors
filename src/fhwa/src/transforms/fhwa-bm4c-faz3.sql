SELECT
    route_id,
    natroute_id,
    state_code,
    CAST(year_record AS INTEGER) AS year_record,
    data_item,
    TRY_CAST(begin_point AS DOUBLE) AS begin_point,
    TRY_CAST(end_point AS DOUBLE) AS end_point,
    value_text,
    TRY_CAST(value_numeric AS DOUBLE) AS value_numeric,
    value_date
FROM "fhwa-bm4c-faz3"
WHERE route_id IS NOT NULL
