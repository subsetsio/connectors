SELECT
    source_entity_id,
    source_endpoint,
    source_url,
    source_file,
    release_name,
    source_modified_date,
    sheet_name,
    row_number,
    column_number,
    cell_ref,
    cell_value
FROM "national-bank-of-rwanda-monthly-exports"
WHERE cell_value IS NOT NULL
